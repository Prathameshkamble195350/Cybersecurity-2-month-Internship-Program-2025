# Termux IPS — Lightweight Intrusion Prevention System (No Root)

A simple **Intrusion Prevention System (IPS)** demo that runs inside **Termux without root**.  
It detects and blocks malicious traffic in **two ways**:
1. **Offline filtering (PCAP analysis):** simulate blocking by splitting packets into `*_allowed.pcap` and `*_blocked.pcap`.  
2. **Proxy mode (user-space enforcement):** run a TCP/HTTP proxy that inspects and blocks suspicious requests in real time (e.g., SQL injection payloads).

---

## 🚀 Features
- Block ICMP ping floods (threshold-based).
- Detect and block TCP SYN floods.
- Detect simple port scans (multiple unique destination ports).
- Block suspicious HTTP payloads (SQLi regex signatures).
- Offline demo with PCAPs (`normal.pcap`, `malicious.pcap`).
- Proxy-mode demo for HTTP services.
- Unit tests (`pytest`).

---

## 📦 Installation (inside Termux)
```bash
pkg update -y && pkg upgrade -y
pkg install -y python git
pip install --upgrade pip
pip install scapy dpkt pytest
