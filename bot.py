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
        # قیمت تتر دلاری از CoinGecko
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd", timeout=8)
        if r.status_code == 200:
            usd_price = r.json()["tether"]["usd"]

            # نرخ تقریبی دلار آزاد (می‌تونی بعداً تغییر بدی یا منبع اضافه کنی)
            dollar_to_toman = 60500  # نرخ تقریبی فعلی (فوریه 2026)

            toman_price = usd_price * dollar_to_toman
            price_str = f"{int(toman_price):,} تومان"
    except Exception as e:
        price_str = f"خطا در CoinGecko: {str(e)}"

    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    msg = f"💰 قیمت تتر الان:\n{price_str}\n\n🕒 {now} (دلاری × تقریبی ۶۰,۵۰۰ تومان)"

    await bot.send_message(chat_id=CHANNEL_ID, text=msg)

    await bot.shutdown()

asyncio.run(main())
