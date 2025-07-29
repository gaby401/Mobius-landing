from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import asyncio
from getpass import getpass

# Telegram API credentials
api_id = 23584803
api_hash = '3dca24c9837a79b699ee038a660b2002'
phone = '+972556676386'

client = TelegramClient('rewardlybot_session', api_id, api_hash)

@client.on(events.NewMessage(from_users='RewardlyBot'))
async def handler(event):
    text = event.raw_text.lower()

    if event.buttons:
        try:
            await event.click(0)
            print("✅ Clicked claim button.")
        except Exception as e:
            print(f"⚠️ Button click failed: {e}")

    if 'doge' in text or 'you earned' in text or 'balance' in text:
        await client.send_message('me', f"📥 [RewardlyBot Update]\n{text}")

async def main():
    print("🔐 Connecting and requesting login code...")

    await client.connect()
    if not await client.is_user_authorized():
        sent = await client.send_code_request(phone)
        code = input("📲 Enter the login code you received via SMS or Telegram: ")
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = getpass("🔐 Enter your 2FA password (it won’t show as you type): ")
            await client.sign_in(password=password)
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return

    print("✅ Logged in successfully. Bot is starting...")

    await client.send_message('RewardlyBot', '/start')
    await asyncio.sleep(5)

    while True:
        try:
            await client.send_message('RewardlyBot', '/claim')
            await asyncio.sleep(3)
            await client.send_message('RewardlyBot', '/balance')
            await asyncio.sleep(300)  # ⏱ 5 minutes = 300 seconds
        except Exception as e:
            print(f"⚠️ Loop error: {e}")
            await asyncio.sleep(30)

client.loop.run_until_complete(main())
client.run_until_disconnected()
