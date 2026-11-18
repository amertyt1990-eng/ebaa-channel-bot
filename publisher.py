import os
import json
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta
from telegram import Bot

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = "@Ebaa_q"

BASE_DIR = Path(__file__).resolve().parent
POSTS_FILE = BASE_DIR / "posts.json"


async def main():
    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        posts = json.load(file)

    if len(posts) < 70:
        raise ValueError("يجب توفير 70 منشوراً على الأقل")

    # توقيت العراق UTC+3
    now = datetime.now(timezone.utc) + timedelta(hours=3)

    # مواعيد التشغيل: الساعة 3، 5، 7 ... 21
    slot = (now.hour - 3) // 2
    slot = max(0, min(slot, 9))

    # تخصيص 10 منشورات لكل يوم
    day_index = now.date().toordinal() % 7
    post_index = day_index * 10 + slot

    post = posts[post_index]

    async with Bot(TOKEN) as bot:
        message = await bot.send_message(
            chat_id=CHANNEL,
            text=post["text"]
        )

    print("تم النشر بنجاح!")
    print("التصنيف:", post["category"])
    print("رقم المنشور:", post_index + 1)
    print("Message ID:", message.message_id)


if __name__ == "__main__":
    asyncio.run(main())
