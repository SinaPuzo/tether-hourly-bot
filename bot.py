import os
import requests
import datetime
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    print("TOKEN یا CHANNEL_ID ست نشده")
    exit(1)

def get_tether_price():
    try:
        r = requests.get("https://api.nobitex.ir/v2/trades/USDTIRT")
        data = r.json()
        price = int(float(data["trades"][0]["price"]))
        return f"{price:,} تومان"
    except Exception as e:
        print("خطا در قیمت:", e)
        return "خطا در دریافت قیمت"

price = get_tether_price()
now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
msg = f"💰 قیمت تتر الان:\n{price}\n\n🕒 {now}"

bot = Bot(token=TOKEN)
bot.send_message(chat_id=CHANNEL_ID, text=msg)
print("پیام ارسال شد:", price)
