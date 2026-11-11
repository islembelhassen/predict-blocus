import os

from dotenv import load_dotenv
from telethon import TelegramClient

from channels import CHANNELS

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient(
    "telegram_session",
    API_ID,
    API_HASH,
)


async def collect_messages(limit=100):
 
    await client.start()

    collected = []

    for channel in CHANNELS:

        messages = await client.get_messages(
            channel["username"],
            limit=limit,
        )

        for msg in messages:

            if not msg.text:
                continue

            collected.append(
                {
                    "channel": channel["name"],
                    "message_id": msg.id,
                    "text": msg.text,
                    "date": msg.date,
                }
            )

    return collected


async def main():

    messages = await collect_messages()

    print(f"{len(messages)} messages found")

    for msg in messages[:5]:
        print(msg)


with client:
    client.loop.run_until_complete(main())