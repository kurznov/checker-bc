from telethon import TelegramClient, events
from telethon import types
import asyncio
from random import randint
from random import choice
import random


checker_api_id = '10373597'
checker_api_hash = '1bb0bbe04bcce67e83c947258f3ce3b5'

sender_api_id = '15013021'
sender_api_hash = '26632e037cb200bfd3ce16bb004da96f'

channel = '@memeklasyalala'
report_group = [-2110070257]

sleep_time = 2  # Seconds

rand_sleep_min = 2 # Seconds
rand_sleep_max = 2 # Seconds

checker_client = TelegramClient('bot', checker_api_id, checker_api_hash)
sender_client= TelegramClient('sender_bot', sender_api_id, sender_api_hash)
posted_messages = {}

@checker_client.on(events.NewMessage(chats=channel))
async def new_message_listener(event):
    posted_messages[event.message.id] = event.message.date

async def check_for_replies():
    while True:
        await asyncio.sleep(sleep_time)
        for msg_id, post_time in posted_messages.copy().items():
            message = await checker_client.get_messages(channel, ids=msg_id)
            
            if int(message.replies.replies) == 0:  
                del posted_messages[msg_id]
                # Forward the message to the report group with a note
                await checker_client.forward_messages(report_group, message.id, channel)
                await checker_client.send_message(report_group, f"afk main-main (start {sleep_time} seconds)")
async def send_random_ping():
    while True:
        await asyncio.sleep(random.randint(rand_sleep_min, rand_sleep_max))
        await sender_client.send_message(channel, "SEND LIST READY")

async def main():
    await checker_client.start()
    await sender_client.start()
    checker_client.loop.create_task(check_for_replies())
    sender_client.loop.create_task(send_random_ping())
    
    await asyncio.gather(
        checker_client.run_until_disconnected(),
        sender_client.run_until_disconnected()
    )

asyncio.run(main())
