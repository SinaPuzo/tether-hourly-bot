import os
import requests
import datetime
import asyncio
from telegram import Bot

async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    if not TOKEN or not CHANNEL_ID:
        msg = "خطا: TOKEN یا CHANNEL_ID موجود نیست"
        bot = Bot(token=TOKEN)
        await bot.initialize()
        await bot.send_message(chat_id=CHANNEL_ID, text=msg)
        return

    bot = Bot(token=TOKEN)
    await bot.initialize()

    price_str = "خطا در دریافت قیمت"

    try:
        url = "https://api.wallex.ir/v1/markets?quote_asset=TMN"
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            try:
                data = r.json()

                # چک کنیم data دیکشنری است یا نه
                if not isinstance(data, dict):
                    price_str = f"پاسخ API دیکشنری نیست: {type(data).__name__}"

                elif "result" not in data:
                    price_str = "کلید 'result' در پاسخ نیست"

                elif not isinstance(data["result"], list):
                    price_str = f"'result' لیست نیست: {type(data['result']).__name__}"

                else:
                    for item in data["result"]:
                        # چک کنیم item دیکشنری است
                        if isinstance(item, dict):
                            symbol = item.get("symbol")
                            if symbol == "USDTTMN":
                                price = item.get("last")
                                if price:
                                    price_str = f"{int(float(price)):,} تومان"
                                    break
                    else:
                        price_str = "جفت USDTTMN پیدا نشد"

            except ValueError as json_err:
                price_str = f"خطا در پارس JSON: {str(json_err)}"
        else:
            price_str = f"خطا در درخواست API (status {r.status_code})"

    except Exception as e:
        price_str = f"خطای کلی: {str(e)}"

    now = datetime.datetime.now().strftime("%H:%M - %Y/%m/%d")
    msg = f"💰 قیمت تتر الان:\n{price_str}\n\n🕒 {now}"

    await bot.send_message(chat_id=CHANNEL_ID, text=msg)

    await bot.shutdown()

asyncio.run(main())
