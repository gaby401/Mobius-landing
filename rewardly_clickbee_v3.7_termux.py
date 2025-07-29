import asyncio
import re
import time
from datetime import datetime
import httpx
from telethon import TelegramClient, events
from telethon.tl.functions.messages import ForwardMessagesRequest

api_id = 23584803
api_hash = '3dca24c9837a79b699ee038a660b2002'
phone_number = '+972556676386'

rewardly_bot = 'RewardlyBot'
clickbee_bot = 'ClickBeeBot'

client = TelegramClient('rewardly_clickbee_v3.7', api_id, api_hash)

async def wait_for_claim_delay(seconds=300):
    print(f"⏱ Waiting {seconds//60} minutes...")
    await asyncio.sleep(seconds)

async def claim_doge():
    try:
        await client.send_message(rewardly_bot, '🎁 Mystery Box 🎁')
        print(f"✅ Clicked RewardlyBot button.")
        await asyncio.sleep(5)
        async for message in client.iter_messages(rewardly_bot, limit=1):
            if 'DOGE' in message.message:
                print(f"🎁 {datetime.now()}: {message.message.strip()}")
    except Exception as e:
        print(f"⚠️ Rewardly failed: {e}")

async def get_url_from_button(message):
    try:
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Open Link" in button.text:
                        return button.url
    except:
        return None
    return None

async def visit_sites():
    print("🌐 Visit Sites - Starting...")
    try:
        await client.send_message(clickbee_bot, '💻 Visit Sites')
        await asyncio.sleep(4)

        async for msg in client.iter_messages(clickbee_bot, limit=5):
            if 'Open Link' in msg.message:
                url = await get_url_from_button(msg)
                if url:
                    print(f"🌐 Visiting: {url}")
                    try:
                        async with httpx.AsyncClient() as session:
                            await session.get(url, timeout=15)
                        print("🕓 Waiting 25 seconds on site...")
                        await asyncio.sleep(25)
                        await client.send_message(clickbee_bot, '🏠 Home')
                        await asyncio.sleep(4)
                        return
                    except Exception as e:
                        print(f"❌ Failed visiting site: {e}")
                else:
                    print("❌ No URL found.")
    except Exception as e:
        print(f"⚠️ Visit Sites error: {e}")

async def join_channels():
    print("📣 Join Channels - Starting...")
    try:
        await client.send_message(clickbee_bot, '📣 Join Channels')
        await asyncio.sleep(6)
        await client.send_message(clickbee_bot, '🏠 Home')
    except Exception as e:
        print(f"❌ Join Channels failed: {e}")

async def join_bots():
    print("🤖 Join Bots - Starting...")
    try:
        await client.send_message(clickbee_bot, '🤖 Join Bots')
        await asyncio.sleep(5)

        async for msg in client.iter_messages(clickbee_bot, limit=5):
            match = re.search(r'https://t\.me/(\w+)\?start=.*', msg.message)
            if match:
                bot_username = match.group(1)
                try:
                    await client.send_message(bot_username, '/start')
                    await asyncio.sleep(5)
                    async for bot_msg in client.iter_messages(bot_username, limit=1):
                        await client.forward_messages(clickbee_bot, bot_msg)
                        print(f"✅ Forwarded bot message from @{bot_username}")
                        await asyncio.sleep(5)
                        return
                except Exception as e:
                    print(f"❌ Bot join failed: {e}")
    except Exception as e:
        print(f"⚠️ Join Bots error: {e}")

async def check_trx_balance():
    try:
        await client.send_message(clickbee_bot, '💰 Balance')
        await asyncio.sleep(4)
        async for msg in client.iter_messages(clickbee_bot, limit=1):
            if 'TRX' in msg.message:
                print(f"💰 {msg.message.strip()}")
    except Exception as e:
        print(f"⚠️ Balance check failed: {e}")

async def main():
    await client.start(phone_number)
    print("✅ Logged in successfully.")
    while True:
        await claim_doge()
        await check_trx_balance()
        await visit_sites()
        await join_channels()
        await join_bots()
        await wait_for_claim_delay(300)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
