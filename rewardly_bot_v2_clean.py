import asyncio
from datetime import datetime
from telethon import TelegramClient, Button

api_id = 23584803
api_hash = '3dca24c9837a79b699ee038a660b2002'
phone_number = '+972556676386'
bot_username = 'RewardlyBot'

client = TelegramClient('rewardly_v2.2_session', api_id, api_hash)

async def click_button_with_text(buttons, keyword):
    for row in buttons:
        for btn in row:
            if keyword.lower() in btn.text.lower():
                await btn.click()
                return True
    return False

async def claim_mystery_box():
    try:
        # Step 1: Click 🎁 Mystery Box 🎁 button
        async for msg in client.iter_messages(bot_username, limit=5):
            if msg.buttons and await click_button_with_text(msg.buttons, "Mystery Box"):
                print("✅ Clicked: 🎁 Mystery Box 🎁")
                await asyncio.sleep(2)
                break
        else:
            print("❌ Couldn't find 🎁 Mystery Box 🎁 button.")
            return

        # Step 2: Look for 'Open Mystery Box'
        await asyncio.sleep(2)
        async for msg in client.iter_messages(bot_username, limit=5):
            if msg.buttons and await click_button_with_text(msg.buttons, "Open Mystery Box"):
                print("✅ Clicked: Open Mystery Box")
                await asyncio.sleep(3)
                async for reply in client.iter_messages(bot_username, limit=1):
                    if 'DOGE' in reply.text:
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"🎁 {now}: {reply.text.strip()}")
                return
        print("❌ Couldn't find 'Open Mystery Box' button.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

async def main():
    await client.start(phone_number)
    print("✅ Logged in successfully.")

    while True:
        await claim_mystery_box()
        print("⏳ Waiting 5 minutes before next claim...\n")
        await asyncio.sleep(300)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
