# update_vps.sh — Auto-update and restart lag agent

#!/bin/bash

# Kill existing agent
echo "[*] Terminating existing agent..."
sudo pkill -f vps_agent.py

# Download latest scripts
echo "[*] Fetching updated scripts from GitHub..."
curl -O https://raw.githubusercontent.com/yourusername/lag-switch-agent/main/vps_agent.py
curl -O https://raw.githubusercontent.com/yourusername/lag-switch-agent/main/dns_amp_spoof.py

# Relaunch agent
echo "[*] Starting updated agent..."
sudo python3 vps_agent.py
