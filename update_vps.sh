#!/bin/bash

echo "[*] Terminating existing agent..."
sudo pkill -f vps_agent.py

echo "[*] Fetching updated scripts from GitHub..."
curl -O https://raw.githubusercontent.com/up5e/lag-switch-agent/main/vps_agent.py
curl -O https://raw.githubusercontent.com/up5e/lag-switch-agent/main/raw_udp_flood.py

echo "[+] Launching updated lag agent..."
sudo python3 vps_agent.py
