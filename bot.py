"""
ربات تلگرام برای ارسال قیمت دلار (و یورو/پوند) به یک کانال، هر ۵ دقیقه یک‌بار.
طراحی‌شده برای اجرای دائمی روی Railway (به‌صورت Worker).

منبع قیمت: Bonbast-API (رایگان و متن‌باز)
https://github.com/itsamirhn/Bonbast-API
"""

import os
import sys
import time
import requests
from datetime import datetime

# ---------- تنظیمات (از Environment Variables خونده می‌شه) ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", 5 * 60))

RATES_API_URL = "https://bonbast.amirhn.com/latest"
# ----------------------------------------------------------------


def get_prices():
    response = requests.get(RATES_API_URL, timeout=10)
    response.raise_for_status()
    return response.json()


def format_message(data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    usd = data.get("usd")
    eur = data.get("eur")
    gbp = data.get("gbp")

    if not usd:
        raise ValueError("قیمت دلار در پاسخ API پیدا نشد")

    lines = [
        "💱 نرخ لحظه‌ای ارز (بازار آزاد)",
        "",
        f"🇺🇸 دلار آمریکا: خرید {usd['buy']:,} | فروش {usd['sell']:,} تومان",
    ]

    if eur:
        lines.append(f"🇪🇺 یورو: خرید {eur['buy']:,} | فروش {eur['sell']:,} تومان")
    if gbp:
        lines.append(f"🇬🇧 پوند: خرید {gbp['buy']:,} | فروش {gbp['sell']:,} تومان")

    lines += ["", f"🕒 بروزرسانی: {now}", "منبع: bonbast.com"]

    return "\n".join(lines)


def send_to_channel(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text}
    response = requests.post(url, data=payload, timeout=10)
    response.raise_for_status()


def main():
    if not BOT_TOKEN or not CHANNEL_ID:
        print("خطا: متغیرهای BOT_TOKEN و CHANNEL_ID تنظیم نشدن.")
        print("این‌ها رو باید در بخش Variables پروژه‌ی Railway ست کنی.")
        sys.exit(1)

    print(f"ربات شروع به کار کرد. هر {INTERVAL_SECONDS} ثانیه قیمت ارسال می‌شود...")
    while True:
        try:
            data = get_prices()
            message = format_message(data)
            send_to_channel(message)
            print(f"[{datetime.now()}] ارسال شد.")
        except Exception as e:
            print(f"[{datetime.now()}] خطا: {e}")

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
