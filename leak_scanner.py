import requests, random, re, time
from bs4 import BeautifulSoup

# 🛡️ Pre-tested working proxies (IP:PORT)
proxies = [
    "138.201.125.229:8080",
    "5.189.184.6:80",
    "91.107.135.210:8080",
    "46.4.96.137:3128",
    "159.203.61.169:8080"
]

# 🎯 Leak pattern definitions
PATTERNS = {
    "mnemonic": r"\b(?:\w+\s){11,23}\w+\b",
    "private_key": r"\b0x[a-fA-F0-9]{64}\b",
    "eth_address": r"\b0x[a-fA-F0-9]{40}\b",
    "btc_address": r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b",
    "jwt": r"\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+\b"
}

# 📡 Leak sources (extendable)
TARGETS = [
    "https://controlc.com/",
    "https://justpaste.it/latest",
    "https://rentry.co/latest"
]

# 🎭 Rotate user agents
def get_headers():
    return {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)",
            "Mozilla/5.0 (Linux; Android 10)"
        ])
    }

# 🔍 Scan page with proxy
def scan_url(url, proxy):
    try:
        r = requests.get(url, headers=get_headers(), timeout=10,
                         proxies={"http": proxy, "https": proxy})
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()
        findings = {}

        for label, pattern in PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                findings[label] = list(set(matches))
        return findings
    except Exception:
        return {}

def main():
    print(f"🔁 Using {len(proxies)} pretested proxies.")
    for target in TARGETS:
        proxy = random.choice(proxies)
        print(f"\n🔍 Scanning {target} using proxy {proxy}...")
        results = scan_url(target, proxy)

        if results:
            print("⚠️ Leaks found:")
            for k, v in results.items():
                print(f"  {k.upper()}: {v}")
        else:
            print("✅ No leak patterns detected.")

        time.sleep(2)

    print("\n✅ Scan complete.")

if __name__ == "__main__":
    main()
