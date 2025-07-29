from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import asyncio
from getpass import getpass
import httpx
from datetime import datetime

api_id = 23584803
api_hash = '3dca24c9837a79b699ee038a660b2002'
phone = '+972556676386'

claim_success = False
client = TelegramClient('rewardlybot_session', api_id, api_hash)

@client.on(events.NewMessage(from_users='RewardlyBot'))
async def rewardly_handler(event):
    global claim_success
    text = event.raw_text.lower()

    if "your mystery box contains" in text:
        claim_success = True
        print(f"🎁 {datetime.now()}: DOGE claimed.")
        await client.send_message('me', f"✅ RewardlyBot:\n{text}")

    if 'doge' in text or 'balance' in text:
        await client.send_message('me', f"📥 RewardlyBot:\n{text}")

    if event.buttons:
        try:
            await event.click(0)
            print("✅ Clicked RewardlyBot button.")
        except Exception as e:
            print(f"⚠️ Rewardly click failed: {e}")

@client.on(events.NewMessage(from_users='ClickBeeBot'))
async def clickbee_handler(event):
    text = event.raw_text.lower()

    if 'visit site' in text and event.buttons:
        try:
            url = event.button_rows[0][0].url
            print(f"🌐 Visiting (fake): {url}")
            async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as c:
                await c.get(url)
            await asyncio.sleep(15)
            await client.send_message('ClickBeeBot', '🏠 Home')
        except Exception as e:
            print(f"⚠️ Site visit failed: {e}")

    elif 'join' in text and 'channel' in text and event.buttons:
        try:
            await event.click(0)
            await asyncio.sleep(5)
            await client.send_message('ClickBeeBot', '✅ Joined')
        except Exception as e:
            print(f"⚠️ Join failed: {e}")

    elif 'trx' in text or 'you earned' in text or 'balance' in text:
        await client.send_message('me', f"💰 ClickBeeBot:\n{text}")

async def clickbee_loop():
    while True:
        await client.send_message('ClickBeeBot', '/start')
        await asyncio.sleep(600)

async def main():
    global claim_success
    print("🔐 Connecting to Telegram...")

    await client.connect()
    if not await client.is_user_authorized():
        sent = await client.send_code_request(phone)
        code = input("📲 Enter code from Telegram: ")
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = getpass("🔐 2FA Password: ")
            await client.sign_in(password=password)
        except Exception as e:
            print(f"❌ Login error: {e}")
            return

    print("✅ Logged in successfully.")
    await client.send_message('RewardlyBot', '/start')
    await asyncio.sleep(5)
    client.loop.create_task(clickbee_loop())

    while True:
        try:
            claim_success = False
            await client.send_message('RewardlyBot', '/claim')
            await asyncio.sleep(5)

            if claim_success:
                print("⏱ Waiting 5 minutes...")
                await asyncio.sleep(300)
            else:
                print("❌ No claim yet. Retrying in 30s...")
                await asyncio.sleep(30)

        except Exception as e:
            print(f"⚠️ Main loop error: {e}")
            await asyncio.sleep(60)

client.loop.run_until_complete(main())
client.run_until_disconnected()
