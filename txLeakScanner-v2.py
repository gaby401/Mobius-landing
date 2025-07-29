#!/usr/bin/env python3

import re
import requests
from datetime import datetime

# Optional: Add your GitHub token to avoid rate limits
GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    # "Authorization": "Bearer ghp_xxxxxxxxxxxxx"  # Uncomment and paste your token here
}

# Leak detection patterns
patterns = {
    "ethereum_private_key": r'(?i)(PRIVATE_KEY|privateKey)\s*=\s*[\'"]?(0x)?[a-f0-9]{64}[\'"]?',
    "mnemonic": r'(?i)(mnemonic|seed)\s*=\s*[\'"]?([a-z]+[\s+]){11,}[a-z]+[\'"]?',
    "raw_signed_tx": r'0x[a-fA-F0-9]{200,}',
    "tx_lib_import": r'(from\s+["\']@ethereumjs/tx["\'])|(require\(["\']@ethereumjs/tx["\']\))',
    "jwt_token": r'eyJ[a-zA-Z0-9-_]{10,}\.[a-zA-Z0-9-_]{10,}\.[a-zA-Z0-9-_]{10,}',
}

# GitHub dork queries
github_dorks = [
    '"PRIVATE_KEY" extension:js',
    '"from \'@ethereumjs/tx\'" extension:ts',
    '"signedTx.serialize()" extension:js',
    '"sign(Buffer.from" extension:js',
    '"mnemonic =" extension:js',
]

# Utility
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# GitHub Scanner
def search_github(query):
    log(f"🔍 GitHub search: {query}")
    url = "https://api.github.com/search/code"
    try:
        res = requests.get(url, headers=GITHUB_HEADERS, params={"q": query, "per_page": 5})
        for item in res.json().get("items", []):
            print(f"\n📂 Repo: {item['repository']['full_name']}")
            print(f"📄 File: {item['name']}\n🔗 {item['html_url']}")
    except Exception as e:
        print(f"❌ GitHub error: {e}")

# Paste site wrappers
def fetch_pastebin():
    try:
        log("🧪 Pastebin scrape...")
        r = requests.get("https://scrape.pastebin.com/api_scraping.php?limit=10", headers={"User-Agent": "Mozilla/5.0"})
        pastes = r.json()
        for p in pastes:
            content = requests.get(p["scrape_url"]).text
            scan_content(content, p["scrape_url"])
    except Exception as e:
        print(f"❌ Pastebin error: {e}")

def fetch_rentry():
    base = "https://rentry.org/"
    urls = ["help", "about", "raw/test"]  # you can seed with real slugs
    for slug in urls:
        try:
            full = f"{base}{slug}"
            r = requests.get(full)
            if r.status_code == 200:
                scan_content(r.text, full)
        except Exception:
            continue

def fetch_controlc():
    try:
        r = requests.get("https://controlc.com/", headers={"User-Agent": "Mozilla/5.0"})
        slugs = re.findall(r'https://controlc\.com/[a-zA-Z0-9]{6}', r.text)
        for url in set(slugs):
            try:
                page = requests.get(url).text
                scan_content(page, url)
            except Exception:
                continue
    except Exception as e:
        print(f"❌ ControlC error: {e}")

def fetch_ghostbin():
    try:
        r = requests.get("https://ghostbin.com/paste", headers={"User-Agent": "Mozilla/5.0"})
        urls = re.findall(r'/p/[a-zA-Z0-9]+', r.text)
        for u in set(urls):
            try:
                raw = f"https://ghostbin.com{u}/raw"
                content = requests.get(raw).text
                scan_content(content, f"https://ghostbin.com{u}")
            except Exception:
                continue
    except Exception as e:
        print(f"❌ Ghostbin error: {e}")

def fetch_justpasteit():
    try:
        r = requests.get("https://justpaste.it/latest", headers={"User-Agent": "Mozilla/5.0"})
        urls = re.findall(r'https://justpaste\.it/[a-zA-Z0-9]+', r.text)
        for url in set(urls):
            try:
                page = requests.get(url).text
                scan_content(page, url)
            except Exception:
                continue
    except Exception as e:
        print(f"❌ JustPaste.it error: {e}")

# Pattern scanner
def scan_content(content, source):
    for label, regex in patterns.items():
        if re.search(regex, content):
            print(f"\n🚨 {label.upper()} match!")
            print(f"🔗 Source: {source}")
            snippet = re.findall(regex, content)
            if snippet:
                print(f"🔍 Snippet: {str(snippet[0])[:100]}...")
            break

# Main
def main():
    log("🚀 Starting txLeakScanner-v2.py")
    for dork in github_dorks:
        search_github(dork)

    log("🌐 Scanning paste sites...")
    fetch_pastebin()
    fetch_rentry()
    fetch_controlc()
    fetch_ghostbin()
    fetch_justpasteit()

    log("✅ Done scanning.")

if __name__ == "__main__":
    main()
