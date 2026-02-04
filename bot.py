import os
import requests
import datetime
import traceback
from telegram import Bot
from telegram.error import TelegramError

print("=== شروع اجرای اسکریپت ===")
print(f"زمان شروع: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print("TELEGRAM_TOKEN دریافت شد؟", "بله (طول:" + str(len(TOKEN or "")) + ")" if TOKEN else "خیر - None")
print("CHANNEL_ID دریافت شد؟", CHANNEL_ID if CHANNEL_ID else "خیر - None")

if not TOKEN or not CHANNEL_ID:
    print("خطای جدی: TOKEN یا CHANNEL_ID موجود نیست")
    exit(1)

try:
    bot = Bot(token=TOKEN)
    print("Bot شیء ساخته شد - bot.id:", bot.id if hasattr(bot, 'id') else "ناموجود")
    print("Bot username:", bot.username if hasattr(bot, 'username') else "ناموجود")

    def get_tether_price():
        print("درخواست قیمت از nobitex شروع شد...")
        try:
            r = requests.get("https://api.nobitex.ir/v2/trades/USDTIRT", timeout=10)
            print("وضعیت پاسخ nobitex:", r.status_code)
            if r.status_code != 200:
                print("پاسخ ناموفق از nobitex:", r.text[:300])
                return "خطا در دریافت قیمت (status " + str(r.status_code) + ")"
            data = r.json()
            print("داده خام trades:", str(data.get("trades", []))[:200])
            if "trades" not in data or not data["trades"]:
                return "هیچ معامله‌ای یافت نشد"
            price = int(float(data["trades"][0]["price"]))
            print("قیمت استخراج شده:", price)
            return f"{price:,} تومان"
        except Exception as e:
            print("خطا در دریافت قیمت:", str(e))
            traceback.print_exc()
            return "خطا در دریافت قیمت"

    price = get_tether_price()
    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    msg = f"💰 قیمت تتر الان:\n{price}\n\n🕒 {now}"

    print("پیام نهایی که می‌خواهد ارسال شود:")
    print("----------------------------------------")
    print(msg)
    print("----------------------------------------")
    print("در حال ارسال به chat_id:", CHANNEL_ID)

    try:
        sent_message = bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode=None)
        print("پیام با موفقیت ارسال شد!")
        print("Message ID:", sent_message.message_id)
        print("Chat ID واقعی:", sent_message.chat.id)
        print("تاریخ ارسال:", sent_message.date)
    except TelegramError as te:
        print("خطای تلگرام (TelegramError):", str(te))
        print("کد خطا:", te.error_code if hasattr(te, 'error_code') else "ناموجود")
        print("توضیح:", te.message if hasattr(te, 'message') else str(te))
        traceback.print_exc()
    except Exception as e:
        print("خطای عمومی در ارسال پیام:", str(e))
        traceback.print_exc()

except Exception as e:
    print("خطای کلی در کل اسکریپت:")
    traceback.print_exc()

print("=== پایان اجرای اسکریپت ===")
