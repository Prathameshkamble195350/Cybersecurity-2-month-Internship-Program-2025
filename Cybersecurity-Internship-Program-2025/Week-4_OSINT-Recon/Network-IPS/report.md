Network IPS — short report
Project: Lightweight Termux IPS (demo)
Duration: 1 week
Author: <Your name>

Objective
---------
Build a lightweight IPS that detects and blocks:
- ICMP ping floods
- TCP SYN floods / half-open connections
- Simple scan patterns (SYN/NULL/FIN / repeated ports)
- Suspicious HTTP payloads (example: SQL injection patterns)

Prevention logic
----------------
1. Packet-source counting:
   - Track per-source counts of SYN (S flag) packets; if count exceeds threshold (SYN_THRESHOLD=20 in demo), mark source as malicious.
   - Track per-source counts of ICMP echo requests; threshold=10.

2. Port-scan detection:
   - Count unique destination ports contacted by a single source. If unique_dest_ports >= 10 within capture → mark as scanner.

3. Payload inspection (application-layer):
   - For TCP flows to HTTP ports, inspect payload (Raw) for SQLi/XSS patterns via regex. If matched → flag and block that source/connection.

4. Enforcement modes:
   - Offline (PCAP filtering): generate `*_blocked.pcap` and `*_allowed.pcap` to demonstrate detection and blocking.
   - Proxy-mode (user-space enforcement): run a TCP/HTTP proxy that inspects and blocks requests for services explicitly routed through it.

False-positives & mitigation
----------------------------
- Simple regex rules lead to FP (e.g., legitimate query strings can contain words like "union"). To reduce FP:
  - Implement whitelists (trusted IPs, known user agents).
  - Use confidence scoring (multiple signals required before blocking).
  - Rate-limit first, then escalate to blocking.
  - Maintain a manual review queue and a time-limited ban (e.g., 10 minutes) rather than permanent block.

Ideas for improvement
---------------------
- Deploy on a gateway with NFQUEUE and python-netfilterqueue for real-time inline blocking (needs root).
- Use sliding-time windows and exponential decay counters for more accurate rate detection.
- Add TLS inspection (via a TLS-terminating proxy) for HTTPS payload inspection (requires cert management).
- Use eBPF/XDP for very high-performance detection on gateways.
- Integrate IP reputation feeds and central logging (ELK/Graylog) + alerting.

Files & tests
-------------
- generate_pcaps.py — creates sample PCAPs (normal + malicious)
- ips_offline.py — offline analyzer that produces allowed/blocked pcap files
- ips_proxy.py — user-space proxy with basic SQLi inspection + rate-limiting
- test_ips.py — pytest unit/integration tests for core detectors
