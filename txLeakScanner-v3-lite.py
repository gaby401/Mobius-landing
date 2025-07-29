#!/usr/bin/env python3

import re, requests, time
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}
GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    # "Authorization": "Bearer ghp_xxxxxxxx"  # optional for higher limits
}

patterns = {
    "eth_private_key": r'(PRIVATE_KEY\s*=\s*[\'"]?(0x)?[a-f0-9]{64})',
    "mnemonic": r'(mnemonic\s*=\s*["\']?([a-z]+\s+){11,}[a-z]+)',
    "raw_signed_tx": r'(0x[a-fA-F0-9]{200,})',
    "jwt_token": r'(eyJ[a-zA-Z0-9-_]{10,}\.[a-zA-Z0-9-_]{10,}\.[a-zA-Z0-9-_]{10,})',
    "infura_key": r'(INFURA_API_KEY\s*=\s*[a-z0-9]{20,})',
    "openai_key": r'(OPENAI_API_KEY\s*=\s*sk-[a-zA-Z0-9]{40,})',
    "eth_address": r'(0x[a-fA-F0-9]{40})'
}

github_dorks = [
    '"PRIVATE_KEY=" extension:env',
    '"mnemonic =" extension:js',
    '"sign(Buffer.from" extension:js',
    '"sk-" extension:env',
]

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_eth_balance(addr):
    try:
        r = requests.get(f"https://api.blockchair.com/ethereum/dashboards/address/{addr}")
        data = r.json()
        balance = int(data["data"][addr.lower()]["address"]["balance"]) / 1e18
        return round(balance, 6)
    except Exception:
        return None

def scan_content(content, source):
    printed = False
    for label, regex in patterns.items():
        matches = re.findall(regex, content)
        if matches:
            if not printed:
                print(f"\n🚨 Leak found in: {source}")
                printed = True
            for m in matches:
                if isinstance(m, tuple): m = m[0]
                print(f"  🔍 {label}: {str(m)[:100]}")
                if label == "eth_address":
                    bal = get_eth_balance(m)
                    if bal and bal > 0:
                        print(f"     💰 ETH Balance: Ξ{bal}")

def search_github(query):
    log(f"🔍 GitHub: {query}")
    try:
        r = requests.get("https://api.github.com/search/code", headers=GITHUB_HEADERS, params={"q": query, "per_page": 5})
        for item in r.json().get("items", []):
            print(f"\n📁 {item['repository']['full_name']}")
            print(f"📄 {item['name']}: {item['html_url']}")
    except Exception as e:
        print(f"❌ GitHub error: {e}")

def fetch_pastebin():
    try:
        log("🧪 Pastebin")
        r = requests.get("https://scrape.pastebin.com/api_scraping.php?limit=10", headers=HEADERS)
        if not r.text.strip().startswith("["): return
        for p in r.json():
            time.sleep(1)
            c = requests.get(p["scrape_url"], headers=HEADERS).text
            scan_content(c, p["scrape_url"])
    except Exception as e:
        print(f"❌ Pastebin error: {e}")

def fetch_generic(base, pattern, raw_fmt=None):
    try:
        r = requests.get(base, headers=HEADERS)
        slugs = re.findall(pattern, r.text)
        for slug in set(slugs):
            try:
                url = raw_fmt(slug) if raw_fmt else slug
                content = requests.get(url, headers=HEADERS).text
                scan_content(content, url)
            except: continue
    except: pass

def fetch_rentry():    fetch_generic("https://rentry.org/", r'/rentry\.org/([a-zA-Z0-9_-]+)', lambda s: f"https://rentry.org/{s}/raw")
def fetch_controlc(): fetch_generic("https://controlc.com/", r'https://controlc\.com/[a-zA-Z0-9]{6}')
def fetch_ghostbin(): fetch_generic("https://ghostbin.com/paste", r'/p/([a-zA-Z0-9]+)', lambda s: f"https://ghostbin.com/p/{s}/raw")
def fetch_justpaste(): fetch_generic("https://justpaste.it/latest", r'https://justpaste\.it/[a-zA-Z0-9]+')

def main():
    log("🚀 txLeakScanner v3-lite started")
    for dork in github_dorks:
        search_github(dork)

    log("🌐 Scanning paste sites...")
    fetch_pastebin()
    fetch_rentry()
    fetch_controlc()
    fetch_ghostbin()
    fetch_justpaste()
    log("✅ Scan complete.")

if __name__ == "__main__":
    main()
