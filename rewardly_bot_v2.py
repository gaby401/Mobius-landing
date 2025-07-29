from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import asyncio
from getpass import getpass

# Telegram API credentials
api_id = 23584803
api_hash = '3dca24c9837a79b699ee038a660b2002'
phone = '+972556676386'

# Global flag to track if a claim was successful
claim_success = False

# Create client session
client = TelegramClient('rewardlybot_session', api_id, api_hash)

@client.on(events.NewMessage(from_users='RewardlyBot'))
async def handler(event):
    global claim_success
    text = event.raw_text.lower()

    # Detect successful DOGE claim
    if "your mystery box contains" in text:
        claim_success = True
        print("🎁 DOGE claimed successfully!")
        await client.send_message('me', f"✅ Mystery Box opened:\n{text}")

    # Forward balance and DOGE info to yourself
    if 'doge' in text or 'balance' in text:
        await client.send_message('me', f"📥 [RewardlyBot Update]\n{text}")

    # Auto-click "🎉 Mystery Box 🎁" button if visible
    if event.buttons:
        try:
            await event.click(0)
            print("✅ Clicked Mystery Box button.")
        except Exception as e:
            print(f"⚠️ Button click failed: {e}")

async def main():
    global claim_success
    print("🔐 Connecting to Telegram...")

    await client.connect()
    if not await client.is_user_authorized():
        sent = await client.send_code_request(phone)
        code = input("📲 Enter the login code you received via SMS or Telegram: ")
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = getpass("🔐 Enter your 2FA password: ")
            await client.sign_in(password=password)
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return

    print("✅ Logged in successfully. Starting RewardlyBot automation...")

    # Kickstart interaction
    await client.send_message('RewardlyBot', '/start')
    await asyncio.sleep(5)

    # Main farming loop
    while True:
        try:
            claim_success = False
            await client.send_message('RewardlyBot', '/claim')
            await asyncio.sleep(5)  # Wait a bit for bot to reply

            if claim_success:
                print("⏱ Waiting full 5 minutes before next claim...")
                await asyncio.sleep(300)
            else:
                print("❌ No claim. Retrying in 30 seconds...")
                await asyncio.sleep(30)

        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            await asyncio.sleep(60)

# Run the client and bot
client.loop.run_until_complete(main())
client.run_until_disconnected()
