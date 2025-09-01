# generate_pcaps.py
from scapy.all import Ether, IP, TCP, ICMP, Raw, wrpcap
import time

def make_normal_pcap(filename="normal.pcap"):
    pkts=[]
    t = time.time()
    p1 = Ether()/IP(src="10.0.0.2", dst="10.0.0.1")/ICMP(type=8)/Raw(load=b'ping')
    p1.time = t
    pkts.append(p1)
    payload = b"GET / HTTP/1.1\r\nHost:example.com\r\n\r\n"
    p2 = Ether()/IP(src="10.0.0.2", dst="10.0.0.1")/TCP(sport=12345, dport=80, flags="PA", seq=1)/Raw(load=payload)
    p2.time = t + 0.1
    pkts.append(p2)
    wrpcap(filename, pkts)
    print(f"Wrote {len(pkts)} packets to {filename}")

def make_malicious_pcap(filename="malicious.pcap"):
    pkts=[]
    t = time.time()
    attacker="192.168.1.200"
    victim="192.168.1.10"
    # SYN flood - 40 SYNs
    for i in range(40):
        p = Ether()/IP(src=attacker, dst=victim)/TCP(sport=40000+i, dport=80, flags="S", seq=1000+i)
        p.time = t + i*0.01
        pkts.append(p)
    # ICMP flood - 30 pings
    for i in range(30):
        p = Ether()/IP(src=attacker, dst=victim)/ICMP(type=8)/Raw(load=b'badping')
        p.time = t + 0.5 + i*0.01
        pkts.append(p)
    # port scan - 15 SYNs from another scanner
    for port in range(2000, 2015):
        p = Ether()/IP(src="192.168.1.201", dst=victim)/TCP(sport=50000+port%1000, dport=port, flags="S")
        p.time = t + 1 + (port-2000)*0.01
        pkts.append(p)
    # HTTP SQLi payload
    sqli = b"POST /login HTTP/1.1\r\nHost:victim\r\nContent-Length:36\r\n\r\nusername=admin' OR '1'='1&password=x"
    p = Ether()/IP(src="192.168.1.202", dst=victim)/TCP(sport=1234, dport=80, flags="PA")/Raw(load=sqli)
    p.time = t + 2
    pkts.append(p)
    wrpcap(filename, pkts)
    print(f"Wrote {len(pkts)} packets to {filename}")

if __name__ == "__main__":
    make_normal_pcap()
    make_malicious_pcap()
