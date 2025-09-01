#!/usr/bin/env python3
# nfqueue_ips.py
import time
import re
from collections import defaultdict, deque
from netfilterqueue import NetfilterQueue
import scapy.all as scapy
from scapy.layers.inet import IP, TCP, ICMP
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Configurable thresholds
SYN_THRESHOLD = 50          # number of SYNs from single IP in WINDOW to consider flood
ICMP_THRESHOLD = 20         # number of ICMP echo requests in WINDOW
PORTSCAN_UNIQUE_PORTS = 15  # unique destination ports within WINDOW to flag as scanner
WINDOW = 10.0               # seconds sliding window for counts
BAN_DURATION = 300          # seconds to keep source banned (simple blacklist)

# SQLi regex (simple demo)
SQLI_RE = re.compile(rb"(union\s+select|'or'|'1'='1|-- |/\*|\bselect\b.*\bfrom\b)", re.IGNORECASE)

# State
syn_times = defaultdict(deque)      # src -> deque of timestamps (SYN)
icmp_times = defaultdict(deque)     # src -> deque timestamps (ICMP echo)
port_history = defaultdict(lambda: defaultdict(deque))  # src -> dport -> deque of times
blacklist = {}                       # src -> unban_time

def now():
    return time.time()

def prune_deque(dq, cutoff):
    while dq and dq[0] < cutoff:
        dq.popleft()

def is_syn_packet(pkt_scapy):
    return TCP in pkt_scapy and (pkt_scapy[TCP].flags & 0x02) and not (pkt_scapy[TCP].flags & 0x10)

def inspect_packet(pkt):
    """
    Return: ('accept'|'drop', reason_string)
    """
    # Convert raw payload into scapy packet
    raw = pkt.get_payload()
    scapy_pkt = scapy.IP(raw)
    if IP not in scapy_pkt:
        return 'accept', 'not ip'

    src = scapy_pkt[IP].src
    cur = now()

    # If already blacklisted
    if src in blacklist:
        if cur < blacklist[src]:
            return 'drop', f'blacklisted until {blacklist[src]}'
        else:
            del blacklist[src]  # unban

    # Track SYNs
    if is_syn_packet(scapy_pkt):
        dq = syn_times[src]
        dq.append(cur)
        prune_deque(dq, cur - WINDOW)
        if len(dq) >= SYN_THRESHOLD:
            blacklist[src] = cur + BAN_DURATION
            logging.warning("SYN flood from %s (count=%d) — banning for %ds", src, len(dq), BAN_DURATION)
            return 'drop', 'syn_flood'

    # Track ICMP echo requests
    if ICMP in scapy_pkt and getattr(scapy_pkt[ICMP], 'type', None) == 8:
        dq = icmp_times[src]
        dq.append(cur)
        prune_deque(dq, cur - WINDOW)
        if len(dq) >= ICMP_THRESHOLD:
            blacklist[src] = cur + BAN_DURATION
            logging.warning("ICMP flood from %s (count=%d) — banning for %ds", src, len(dq), BAN_DURATION)
            return 'drop', 'icmp_flood'

    # Port-scan detection (unique destination ports)
    if TCP in scapy_pkt:
        dport = int(scapy_pkt[TCP].dport)
        ph = port_history[src][dport]
        ph.append(cur)
        # cleanup entries per port older than WINDOW
        prune_deque(ph, cur - WINDOW)
        # Count unique ports with activity in WINDOW
        unique_ports = 0
        for p, dq in port_history[src].items():
            prune_deque(dq, cur - WINDOW)
            if dq:
                unique_ports += 1
        if unique_ports >= PORTSCAN_UNIQUE_PORTS:
            blacklist[src] = cur + BAN_DURATION
            logging.warning("Port-scan from %s (unique_ports=%d) — banning for %ds", src, unique_ports, BAN_DURATION)
            return 'drop', 'port_scan'

    # Payload inspection for SQLi (only for TCP, and when payload present)
    if scapy.Raw in scapy_pkt:
        payload_bytes = bytes(scapy_pkt[scapy.Raw].load)
        if SQLI_RE.search(payload_bytes):
            blacklist[src] = cur + BAN_DURATION
            logging.warning("SQLi payload from %s — banning for %ds", src, BAN_DURATION)
            return 'drop', 'sqli'

    return 'accept', 'ok'

def nfqueue_callback(packet):
    try:
        action, reason = inspect_packet(packet)
        if action == 'drop':
            # drop packet
            packet.drop()
            logging.info("Dropped packet from %s — reason=%s", packet.get_src(), reason)
        else:
            # accept packet
            packet.accept()
    except Exception as e:
        logging.exception("Exception in callback: %s", e)
        # default to accept to reduce risk of network outage
        packet.accept()

def sigint_handler(sig, frame):
    logging.info("Shutting down NFQUEUE IPS...")
    nfqueue.unbind()
    sys.exit(0)

if __name__ == "__main__":
    nfqueue = NetfilterQueue()
    try:
        nfqueue.bind(1, nfqueue_callback)   # queue number 1 must match iptables rule
        signal.signal(signal.SIGINT, sigint_handler)
        logging.info("NFQUEUE IPS bound to queue 1. Running...")
        nfqueue.run()
    except KeyboardInterrupt:
        sigint_handler(None, None)
    except Exception as e:
        logging.exception("Fatal error: %s", e)
        try:
            nfqueue.unbind()
        except:
            pass
