#!/bin/bash
for f in test_pcaps/*.pcap; do
  echo "Processing $f"
  python3 network_ids.py "$f"
  echo ""
done
