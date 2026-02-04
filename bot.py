import os
import requests
import datetime
import asyncio
from telegram import Bot
from telegram.error import TelegramError

async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    if not TOKEN or not CHANNEL_ID:
        print("TOKEN یا CHANNEL_ID موجود نیست")
        return

    bot = Bot(token=TOKEN)
    await bot.initialize()

    try:
        # قیمت از Wallex
        r = requests.get("https://api.wallex.ir/v1/currencies/stats?quote_asset=IRT", timeout=10)
        if r.status_code == 200:
            data = r.json()
            usdt = data.get("result", {}).get("USDT", {}).get("stats", {})
            price = usdt.get("last") or usdt.get("latest")
            if price:
                price_str = f"{int(float(price)):,} تومان"
            else:
                price_str = "خطا در داده Wallex"
        else:
            price_str = f"خطا API Wallex (status {r.status_code})"

        now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
        msg = f"💰 قیمت تتر الان:\n{price_str}\n\n🕒 {now}"

        await bot.send_message(chat_id=CHANNEL_ID, text=msg)
        print("پیام ارسال شد")

        await bot.shutdown()

    except Exception as e:
        print("خطا:", str(e))
        await bot.send_message(chat_id=CHANNEL_ID, text=f"خطا در اجرا: {str(e)}")

asyncio.run(main())
