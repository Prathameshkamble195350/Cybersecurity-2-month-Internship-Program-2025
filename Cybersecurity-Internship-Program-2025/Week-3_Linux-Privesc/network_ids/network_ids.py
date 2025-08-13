#!/usr/bin/env python3

from scapy.all import rdpcap, IP, TCP, ICMP
import sys

# Thresholds for alerts
ICMP_FLOOD_THRESHOLD = 10
SYN_SCAN_THRESHOLD = 10

icmp_counts = {}
syn_counts = {}

def detect_packet(pkt):
    if IP not in pkt:
        return

    ip = pkt[IP]
    src = ip.src
    dst = ip.dst

    if pkt.haslayer(ICMP):
        icmp_counts[src] = icmp_counts.get(src, 0) + 1
        print(f"[ICMP] Ping from {src} to {dst} (Count: {icmp_counts[src]})")
        if icmp_counts[src] > ICMP_FLOOD_THRESHOLD:
            print(f"[ALERT] Possible ICMP flood from {src}!")

    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        if tcp.flags == 'S':  # SYN flag only
            syn_counts[src] = syn_counts.get(src, 0) + 1
            print(f"[TCP] SYN from {src} to port {tcp.dport} (Count: {syn_counts[src]})")
            if syn_counts[src] > SYN_SCAN_THRESHOLD:
                print(f"[ALERT] Possible SYN scan from {src}!")

def main():
    if len(sys.argv) != 2:
          
