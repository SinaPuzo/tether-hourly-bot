import os
import requests
import datetime
import asyncio
from telegram import Bot

async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    bot = Bot(token=TOKEN)
    await bot.initialize()

    price_str = "قیمت پیدا نشد"

    try:
        r = requests.get("https://api.wallex.ir/v1/markets", timeout=10)
        data = r.json()
        usdt = data["result"]["USDTTMN"]
        price = usdt["stats"]["lastPrice"]
        price_str = f"{int(float(price)):,} تومان"
    except:
        pass  # اگر هر مشکلی بود، همون پیام پیش‌فرض می‌مونه

    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    msg = f"💰 قیمت تتر الان:\n{price_str}\n\n🕒 {now}"

    await bot.send_message(chat_id=CHANNEL_ID, text=msg)

    await bot.shutdown()

asyncio.run(main())
