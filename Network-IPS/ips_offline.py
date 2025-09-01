# ips_offline.py
from scapy.all import rdpcap, wrpcap, IP, TCP, ICMP, Raw
import re, sys

SYN_THRESHOLD = 20
ICMP_THRESHOLD = 10
PORTSCAN_THRESHOLD = 10
SQLI_PAT = re.compile(rb"(union\s+select|'or'|'1'='1|-- |/\*|\bselect\b.*\bfrom\b)", re.IGNORECASE)

def is_syn(pkt):
    if TCP in pkt:
        flags = int(pkt[TCP].flags)
        return bool(flags & 0x02) and not bool(flags & 0x10)
    return False

def payload_matches_sqli(pkt):
    if Raw in pkt and TCP in pkt:
        data = bytes(pkt[Raw].load)
        return SQLI_PAT.search(data) is not None
    return False

def analyze_and_filter(pcapfile, out_prefix=None):
    if out_prefix is None:
        out_prefix = pcapfile.replace('.pcap','')
    pkts = rdpcap(pcapfile)
    print(f"[+] Loaded {len(pkts)} packets from {pcapfile}")
    syn_counts = {}
    icmp_counts = {}
    src_ports = {}
    sqli_flagged = set()
    for pkt in pkts:
        if IP not in pkt:
            continue
        src = pkt[IP].src
        if is_syn(pkt):
            syn_counts[src] = syn_counts.get(src, 0) + 1
            src_ports.setdefault(src, set()).add(int(pkt[TCP].dport))
        if ICMP in pkt:
            if pkt[ICMP].type == 8:
                icmp_counts[src] = icmp_counts.get(src, 0) + 1
        if payload_matches_sqli(pkt):
            sqli_flagged.add(src)
    blocked_srcs = set()
    for src, c in syn_counts.items():
        if c >= SYN_THRESHOLD:
            blocked_srcs.add(src)
    for src, c in icmp_counts.items():
        if c >= ICMP_THRESHOLD:
            blocked_srcs.add(src)
    for src, ports in src_ports.items():
        if len(ports) >= PORTSCAN_THRESHOLD:
            blocked_srcs.add(src)
    blocked_srcs |= sqli_flagged

    allowed=[]
    blocked=[]
    for pkt in pkts:
        if IP not in pkt:
            allowed.append(pkt)
            continue
        if pkt[IP].src in blocked_srcs:
            blocked.append(pkt)
        else:
            if payload_matches_sqli(pkt):
                blocked.append(pkt); blocked_srcs.add(pkt[IP].src)
            else:
                allowed.append(pkt)
    allowed_file = f"{out_prefix}_allowed.pcap"
    blocked_file = f"{out_prefix}_blocked.pcap"
    wrpcap(allowed_file, allowed)
    wrpcap(blocked_file, blocked)
    print(f"[+] Blocked sources: {blocked_srcs}")
    print(f"[+] Wrote allowed -> {allowed_file} ({len(allowed)} pkts)")
    print(f"[+] Wrote blocked -> {blocked_file} ({len(blocked)} pkts)")
    return {"blocked_srcs": blocked_srcs, "allowed_count": len(allowed), "blocked_count": len(blocked)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ips_offline.py <pcapfile> [out_prefix]")
        sys.exit(1)
    analyze_and_filter(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None)
