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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        r = requests.get("https://api.nobitex.ir/v2/trades/USDTIRT", headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if "trades" in data and data["trades"]:
                price = data["trades"][0]["price"]
                price_str = f"{int(float(price)):,} تومان"
    except:
        pass

    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    msg = f"💰 قیمت تتر الان:\n{price_str}\n\n🕒 {now}"

    await bot.send_message(chat_id=CHANNEL_ID, text=msg)

    await bot.shutdown()

asyncio.run(main())
