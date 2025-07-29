import asyncio
import re
import time
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = 23584803
api_hash = '3dca24c9837a79b699ee038a660b2002'
phone_number = '+972556676386'

rewardly_bot = 'RewardlyBot'
clickbee_bot = 'ClickBeeBot'

client = TelegramClient('session', api_id, api_hash)

async def wait_for_claim_delay(seconds=300):
    print(f"⏱ Waiting {seconds//60} minutes...")
    await asyncio.sleep(seconds)

async def claim_doge():
    await client.send_message(rewardly_bot, '🎁 Mystery Box 🎁')
    print(f"✅ Clicked RewardlyBot button.")
    await asyncio.sleep(5)
    async for message in client.iter_messages(rewardly_bot, limit=1):
        if 'DOGE' in message.message:
            print(f"🎁 {datetime.now()}: {message.message.strip()}")

async def get_clickbee_button(message, label_keywords):
    if not message.buttons:
        return None
    for row in message.buttons:
        for button in row:
            if any(k.lower() in button.text.lower() for k in label_keywords):
                return button
    return None

async def complete_visit_sites():
    print("🌐 Starting ClickBeeBot: Visit Sites")
    await client.send_message(clickbee_bot, '💻 Visit Sites')
    await asyncio.sleep(4)

    async for msg in client.iter_messages(clickbee_bot, limit=3):
        if 'Open Link' in msg.message:
            open_link_btn = await get_clickbee_button(msg, ['Open Link'])
            if open_link_btn:
                try:
                    await msg.click(text=open_link_btn.text)
                    print("🌐 Clicked Open Link")
                    await asyncio.sleep(25)  # Simulate browsing
                    await client.send_message(clickbee_bot, '🏠 Home')
                    print("🏠 Returned Home")
                    return
                except Exception as e:
                    print(f"❌ Open Link failed: {e}")
        elif 'No new ads' in msg.message:
            print("🚫 No Visit Sites available.")
            return

async def join_channels():
    print("📣 Starting Join Channels task...")
    await client.send_message(clickbee_bot, '📣 Join Channels')
    await asyncio.sleep(5)
    async for msg in client.iter_messages(clickbee_bot, limit=3):
        join_btn = await get_clickbee_button(msg, ['Join'])
        if join_btn:
            try:
                await msg.click(text=join_btn.text)
                await asyncio.sleep(8)
                await client.send_message(clickbee_bot, '🏠 Home')
                print("✅ Joined Channel and returned Home.")
                return
            except Exception as e:
                print(f"❌ Join Channel failed: {e}")

async def join_bots():
    print("🤖 Starting Join Bots task...")
    await client.send_message(clickbee_bot, '🤖 Join Bots')
    await asyncio.sleep(5)
    async for msg in client.iter_messages(clickbee_bot, limit=3):
        bot_btn = await get_clickbee_button(msg, ['Start', 'Join'])
        if bot_btn:
            try:
                await msg.click(text=bot_btn.text)
                await asyncio.sleep(10)
                await client.send_message(clickbee_bot, '🏠 Home')
                print("✅ Joined Bot and returned Home.")
                return
            except Exception as e:
                print(f"❌ Join Bot failed: {e}")

async def check_trx_balance():
    await client.send_message(clickbee_bot, '💰 Balance')
    await asyncio.sleep(3)
    async for msg in client.iter_messages(clickbee_bot, limit=1):
        if 'TRX' in msg.message:
            print(f"💰 TRX Balance: {msg.message.strip()}")
            return

async def main():
    await client.start(phone_number)
    print("✅ Logged in successfully.")
    while True:
        await claim_doge()
        await check_trx_balance()
        await complete_visit_sites()
        await join_channels()
        await join_bots()
        await wait_for_claim_delay(300)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
