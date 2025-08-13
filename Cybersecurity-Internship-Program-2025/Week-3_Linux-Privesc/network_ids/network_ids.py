#!/usr/bin/env python3

from scapy.all import rdpcap, IP, TCP, ICMP
import sys

# Thresholds for alerts
ICMP_FLOOD_THRESHOLD = 10
SYN_SCAN_THRESHOLD = 10

# Dictionaries to keep track of counts per source IP
icmp_counts = {}
syn_counts = {}

def detect_packet(pkt):
    """Analyze a single packet for ICMP flood or TCP SYN scan."""
    if IP not in pkt:
        return

    ip = pkt[IP]
    src = ip.src
    dst = ip.dst

    # ICMP detection
    if pkt.haslayer(ICMP):
        icmp_counts[src] = icmp_counts.get(src, 0) + 1
        print(f"[ICMP] Ping from {src} to {dst} (Count: {icmp_counts[src]})")
        if icmp_counts[src] > ICMP_FLOOD_THRESHOLD:
            print(f"[ALERT] Possible ICMP flood from {src}!")

    # TCP SYN detection
    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        if tcp.flags == 'S':  # SYN flag only
            syn_counts[src] = syn_counts.get(src, 0) + 1
            print(f"[TCP] SYN from {src} to port {tcp.dport} (Count: {syn_counts[src]})")
            if syn_counts[src] > SYN_SCAN_THRESHOLD:
                print(f"[ALERT] Possible SYN scan from {src}!")

def main():
    """Main function to read pcap file and process packets."""
    # Check command-line arguments
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pcap_file>")
        sys.exit(1)

    pcap_file = sys.argv[1]

    # Read pcap file
    try:
        packets = rdpcap(pcap_file)
    except FileNotFoundError:
        print(f"Error: File '{pcap_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Process each packet
    for pkt in packets:
        detect_packet(pkt)

if __name__ == "__main__":
    main()          
