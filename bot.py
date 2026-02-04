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
        # قیمت تتر دلاری
        r_tether = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd", timeout=8)
        usd_price = r_tether.json()["tether"]["usd"]

        # نرخ دلار آزاد از منبع ساده (مثال: api.arzdigital یا tgju)
        r_dollar = requests.get("https://api.arzdigital.com/api/v1/currencies/usd", timeout=8)
        if r_dollar.status_code == 200:
            dollar_data = r_dollar.json()
            dollar_price = dollar_data.get("price", 92000)  # اگر خطا داد، پیش‌فرض
        else:
            dollar_price = 92000  # پیش‌فرض

        toman_price = usd_price * dollar_price
        price_str = f"{int(toman_price):,} تومان"

    except Exception as e:
        price_str = f"خطا: {str(e)}"

    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    msg = f"💰 قیمت تتر الان:\n{price_str}\n\n🕒 {now} (CoinGecko + نرخ دلار)"

    await bot.send_message(chat_id=CHANNEL_ID, text=msg)

    await bot.shutdown()

asyncio.run(main())
