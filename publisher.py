
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta

from telegram import Bot
from telegram.request import HTTPXRequest
from telegram.error import NetworkError

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = "@Ebaa_q"

BASE_DIR = Path(__file__).resolve().parent
POSTS_FILE = BASE_DIR / "posts.json"


async def main():
    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        posts = json.load(file)

    if len(posts) < 70:
        raise ValueError("يجب توفير 70 منشوراً على الأقل")

    now = datetime.now(timezone.utc) + timedelta(hours=3)

    slot = (now.hour - 3) // 2
    slot = max(0, min(slot, 9))

    day_index = now.date().toordinal() % 7
    post_index = day_index * 10 + slot

    post = posts[post_index]

    for attempt in range(1, 4):
        try:
            request = HTTPXRequest(
                connection_pool_size=8,
                connect_timeout=30,
                read_timeout=60,
                write_timeout=60,
                pool_timeout=30
            )

            async with Bot(TOKEN, request=request) as bot:
                message = await bot.send_message(
                    chat_id=CHANNEL,
                    text=post["text"],
                    connect_timeout=30,
                    read_timeout=60,
                    write_timeout=60,
                    pool_timeout=30
                )

            print("تم النشر بنجاح!")
            print("التصنيف:", post["category"])
            print("رقم المنشور:", post_index + 1)
            print("Message ID:", message.message_id)
            return

        except NetworkError as error:
            print(f"فشلت المحاولة {attempt}: {error}")

            if attempt == 3:
                raise

            await asyncio.sleep(10 * attempt)


if __name__ == "__main__":
    asyncio.run(main())
