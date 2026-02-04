import os
import requests
import asyncio
import jdatetime
from telegram import Bot

async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    if not TOKEN or not CHANNEL_ID:
        print("TOKEN یا CHANNEL_ID ست نشده")
        return

    bot = Bot(token=TOKEN)
    await bot.initialize()

    try:
        # OMP Finex – USDT/IRT
        url = "https://api.ompfinex.com/v1/market/ticker?symbol=USDTIRT"
        r = requests.get(url, timeout=10)
        data = r.json()

        last_price = data["result"]["last"]
        price = f"{int(float(last_price)):,} تومان"

    except Exception as e:
        price = f"خطا: {e}"

    # تاریخ شمسی (بدون ساعت)
    date_shamsi = jdatetime.date.today().strftime("%Y/%m/%d")

    msg = f"{price}\n{date_shamsi}"

    await bot.send_message(chat_id=CHANNEL_ID, text=msg)
    await bot.shutdown()

asyncio.run(main())
