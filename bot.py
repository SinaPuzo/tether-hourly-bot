import os
import requests
import datetime
import asyncio
from telegram import Bot

async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    if not TOKEN or not CHANNEL_ID:
        print("TOKEN یا CHANNEL_ID ست نشده")
        return

    bot = Bot(token=TOKEN)
    await bot.initialize()

    price_str = "خطا در دریافت قیمت"

    try:
        url = "https://api.wallex.ir/v1/markets?quote_asset=TMN"
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            data = r.json()

            # مسیر صحیح JSON
            usdt_market = data["result"]["symbols"].get("USDTTMN")

            if usdt_market:
                last_price = usdt_market["stats"].get("lastPrice")
                if last_price:
                    price_str = f"{int(float(last_price)):,} تومان"
                else:
                    price_str = "lastPrice پیدا نشد"
            else:
                price_str = "USDTTMN پیدا نشد"
        else:
            price_str = f"خطای API: {r.status_code}"

    except Exception as e:
        price_str = f"خطا: {e}"

    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    msg = f"💰 قیمت تتر:\n{price_str}\n\n🕒 {now}"

    await bot.send_message(chat_id=CHANNEL_ID, text=msg)
    await bot.shutdown()

asyncio.run(main())
