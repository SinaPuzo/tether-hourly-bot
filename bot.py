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
        print("درخواست به Wallex markets...")
        r = requests.get("https://api.wallex.ir/v1/markets?quote_asset=IRT", timeout=10)
        print("وضعیت پاسخ:", r.status_code)
        print("محتوای خام پاسخ (اول 300 کاراکتر):")
        print(r.text[:300])

        price_str = "خطا در API Wallex"

        if r.status_code == 200:
            try:
                data = r.json()
                print("پاسخ JSON شد. نوع data:", type(data))
                if isinstance(data, dict) and "result" in data:
                    for market in data["result"]:
                        if isinstance(market, dict) and market.get("base_asset") == "USDT":
                            price = market.get("last")
                            if price:
                                price_str = f"{int(float(price)):,} تومان"
                                break
                    else:
                        price_str = "USDT در لیست پیدا نشد"
                else:
                    price_str = "پاسخ JSON معتبر نبود"
            except Exception as json_err:
                price_str = f"خطا در تبدیل به JSON: {str(json_err)}"
        else:
            price_str = f"خطا Wallex status {r.status_code}"

        now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
        msg = f"💰 قیمت تتر الان:\n{price_str}\n\n🕒 {now}"

        await bot.send_message(chat_id=CHANNEL_ID, text=msg)
        print("پیام ارسال شد")

        await bot.shutdown()

    except Exception as e:
        print("خطای کلی:", str(e))
        await bot.send_message(chat_id=CHANNEL_ID, text=f"خطا در اجرا: {str(e)}")

asyncio.run(main())
