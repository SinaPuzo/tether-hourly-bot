import os
import requests
import datetime
import asyncio
from telegram import Bot
from telegram.error import TelegramError

print("=== شروع اجرای اسکریپت ===")
print(f"زمان شروع: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print("TELEGRAM_TOKEN دریافت شد؟", "بله (طول:" + str(len(TOKEN or "")) + ")" if TOKEN else "خیر")
print("CHANNEL_ID دریافت شد؟", CHANNEL_ID if CHANNEL_ID else "خیر")

if not TOKEN or not CHANNEL_ID:
    print("خطا: TOKEN یا CHANNEL_ID ست نشده")
    exit(1)

async def main():
    try:
        bot = Bot(token=TOKEN)
        print("Bot ساخته شد")

        # این خط خیلی مهمه - initialize کردن bot
        await bot.initialize()
        print("Bot initialize شد")

        # اطلاعات bot رو چک می‌کنیم
        me = await bot.get_me()
        print("Bot username:", me.username)
        print("Bot id:", me.id)

        # گرفتن قیمت
        print("گرفتن قیمت تتر...")
        try:
            r = requests.get("https://api.nobitex.ir/v2/trades/USDTIRT", timeout=10)
            print("وضعیت API:", r.status_code)
            data = r.json()
            if "trades" in data and data["trades"]:
                price = int(float(data["trades"][0]["price"]))
                print("قیمت:", price)
            else:
                price = None
                print("هیچ معامله‌ای پیدا نشد")
        except Exception as e:
            print("خطا در گرفتن قیمت:", str(e))
            price = None

        if price:
            now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
            msg = f"💰 قیمت تتر الان:\n{price:,} تومان\n\n🕒 {now}"
        else:
            msg = "خطا در دریافت قیمت تتر"

        print("پیام آماده ارسال:")
        print(msg)
        print("ارسال به:", CHANNEL_ID)

        # ارسال پیام
        sent = await bot.send_message(chat_id=CHANNEL_ID, text=msg)
        print("پیام ارسال شد ✓")
        print("Message ID:", sent.message_id)

        # بستن bot
        await bot.shutdown()

    except TelegramError as te:
        print("خطای تلگرام:", str(te))
        print("error_code:", getattr(te, 'error_code', 'ندارد'))
    except Exception as e:
        print("خطای کلی:", str(e))

# اجرا
asyncio.run(main())

print("=== پایان اسکریپت ===")
