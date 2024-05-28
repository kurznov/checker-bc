from telethon import TelegramClient, events
from telethon import types
import asyncio
from random import randint
from random import choice
import random


checker_api_id = '23630005'
checker_api_hash = 'cd24b2a07a9dfa52e4adcd99f41c8d4a'

sender_api_id = '16738665'
sender_api_hash = 'a58405e7f07ab8f3ca0a5d3aef7c6323'

channel = '@chtest88088'
report_group = '@test88088'

sleep_time = 2 * 60  # Seconds

rand_sleep_min = 4 * 60 # Seconds
rand_sleep_max = 8 * 60 # Seconds

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
                await checker_client.send_message(report_group, f"No Replies detected for the message above after {sleep_time} seconds.")
async def send_random_ping():
    while True:
        await asyncio.sleep(random.randint(rand_sleep_min, rand_sleep_max))
        await sender_client.send_message(channel, "PING")

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
