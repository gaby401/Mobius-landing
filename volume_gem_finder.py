#!/usr/bin/env python3
import requests
import json

def fetch_coins(pages=4):
    all_coins = []
    for page in range(1, pages + 1):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_asc",
            "per_page": 250,
            "page": page,
            "price_change_percentage": "24h"
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            all_coins.extend(response.json())
        except Exception as e:
            print(f"Error on page {page}:", e)
    return all_coins

def filter_and_sort_gems(coins):
    filtered = []
    for coin in coins:
        mc = coin['market_cap']
        vol = coin['total_volume']
        if mc and vol and mc < 100_000_000:
            ratio = vol / mc
            filtered.append({
                "name": coin['name'],
                "symbol": coin['symbol'],
                "mc": mc,
                "volume": vol,
                "vol/mc %": round(ratio * 100, 2)
            })
    return sorted(filtered, key=lambda x: x["vol/mc %"], reverse=True)[:15]

def display_gems(gems):
    print(f"\n📊 Top {len(gems)} low cap coins by Volume/MarketCap ratio:\n")
    for g in gems:
        print(f"{g['name']} ({g['symbol'].upper()}): MC ${g['mc']:,}, Volume ${g['volume']:,}, Vol/MC: {g['vol/mc %']}%")

def save_to_json(gems):
    with open("volume_gems.json", "w") as f:
        json.dump(gems, f, indent=2)
    print("\n💾 Saved to volume_gems.json")

if __name__ == "__main__":
    coins = fetch_coins()
    gems = filter_and_sort_gems(coins)
    display_gems(gems)
    if gems:
        save_to_json(gems)
