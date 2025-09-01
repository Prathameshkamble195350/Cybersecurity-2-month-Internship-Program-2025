# test_ips.py
import pytest
from scapy.all import IP, TCP, Raw
import ips_offline as ips

def test_is_syn():
    pkt = IP(src='1.1.1.1')/TCP(dport=80, flags='S')
    assert ips.is_syn(pkt)

def test_payload_sqli():
    pkt = IP(src='2.2.2.2')/TCP(dport=80)/Raw(load=b"username=admin' OR '1'='1")
    assert ips.payload_matches_sqli(pkt)

def test_analyze_filter_small(tmp_path):
    pkts=[]
    for i in range(25):
        pkts.append(IP(src='9.9.9.9')/TCP(dport=80,flags='S'))
    pcap_file = tmp_path / "tmp_test.pcap"
    from scapy.utils import wrpcap
    wrpcap(str(pcap_file), pkts)
    res = ips.analyze_and_filter(str(pcap_file), out_prefix=str(tmp_path/'tmp_test'))
    assert '9.9.9.9' in res['blocked_srcs']
