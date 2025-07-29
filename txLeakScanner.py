#!/usr/bin/env python3
# txLeakScanner.py

import re
import requests
from datetime import datetime
from urllib.parse import quote

GITHUB_SEARCH_URL = "https://api.github.com/search/code"
PASTEBIN_SCRAPE_URL = "https://scrape.pastebin.com/api_scraping.php?limit=10"

GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer YOUR_GITHUB_TOKEN"  # optional, increases rate limit
}

# Regex patterns for key leaks
patterns = {
    "private_key": r'(?i)(PRIVATE_KEY|privateKey)\s*=\s*[\'"]?(0x)?[a-f0-9]{64}[\'"]?',
    "mnemonic": r'(?i)(mnemonic|seed)\s*=\s*[\'"]?([a-z]+[\s+]){11,}[a-z]+[\'"]?',
    "signed_tx": r'0x[a-fA-F0-9]{200,}',  # crude heuristic for raw tx
    "tx_import": r'(from\s+["\']@ethereumjs/tx["\'])|(require\(["\']@ethereumjs/tx["\']\))'
}


def search_github(query):
    print(f"[{datetime.now()}] 🔍 GitHub search: {query}")
    params = {"q": query, "per_page": 5}
    response = requests.get(GITHUB_SEARCH_URL, headers=GITHUB_HEADERS, params=params)
    for item in response.json().get("items", []):
        print(f"\n📁 {item['repository']['full_name']}")
        print(f"📄 {item['name']}: {item['html_url']}")


def scan_pastebin():
    print(f"[{datetime.now()}] 🧪 Scanning Pastebin latest pastes...")
    try:
        res = requests.get(PASTEBIN_SCRAPE_URL)
        for paste in res.json():
            content = requests.get(paste['scrape_url']).text
            for name, regex in patterns.items():
                if re.search(regex, content):
                    print(f"\n🚨 {name.upper()} found in Pastebin!")
                    print(f"🔗 {paste['scrape_url']}")
                    break
    except Exception as e:
        print(f"❌ Pastebin error: {e}")


def main():
    github_dorks = [
        '"PRIVATE_KEY" extension:js',
        '"from \'@ethereumjs/tx\'" extension:ts',
        '"signedTx.serialize()" extension:js',
        '"sign(Buffer.from" extension:js',
        '"mnemonic =" extension:js',
    ]

    for dork in github_dorks:
        search_github(dork)

    scan_pastebin()


if __name__ == "__main__":
    main()
