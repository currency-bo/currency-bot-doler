# ربات تلگرام قیمت دلار

این ربات هر ۵ دقیقه یک‌بار قیمت دلار (و یورو/پوند) رو از منبع رایگان
[Bonbast-API](https://github.com/itsamirhn/Bonbast-API) می‌گیره و به یه کانال
تلگرام ارسال می‌کنه.

## مرحله ۱: ساخت ربات تلگرام

1. توی تلگرام برو پیش [@BotFather](https://t.me/BotFather)
2. دستور `/newbot` رو بزن و اسم و یوزرنیم برای ربات انتخاب کن
3. یه توکن بهت می‌ده شبیه `123456789:ABCdefGhIJKlmNoPQRstuVwxYZ` — این همون `BOT_TOKEN`ه
4. ربات رو به کانالت اضافه کن و بهش دسترسی **ادمین** (با اجازه‌ی ارسال پیام) بده
5. آیدی کانال (`CHANNEL_ID`) رو مشخص کن:
   - اگه کانال یوزرنیم عمومی داره: چیزی شبیه `@your_channel`
   - اگه خصوصیه: یه پیام از کانال رو به [@userinfobot](https://t.me/userinfobot) فوروارد کن تا chat_id عددی (مثل `-1001234567890`) بگیری

## مرحله ۲: آپلود پروژه روی گیت‌هاب

```bash
git init
git add .
git commit -m "Initial commit: Telegram dollar price bot"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

> نکته: فایل `BOT_TOKEN` هیچ‌جای کد نوشته نشده — این مقدار حساسه و فقط توی
> تنظیمات Railway (نه توی گیت‌هاب) ست می‌شه، پس نگران لو رفتنش نباش.

## مرحله ۳: دیپلوی روی Railway

1. وارد [railway.app](https://railway.app) شو و با اکانت گیت‌هابت وارد شو
2. **New Project** → **Deploy from GitHub repo** رو بزن و ریپازیتوری‌ای که
   ساختی رو انتخاب کن
3. Railway به‌صورت خودکار `requirements.txt` و `Procfile` رو تشخیص می‌ده
4. برو به تب **Variables** پروژه و این دو متغیر رو اضافه کن:
   - `BOT_TOKEN` = توکنی که از BotFather گرفتی
   - `CHANNEL_ID` = آیدی کانالت
   - (اختیاری) `INTERVAL_SECONDS` = فاصله‌ی زمانی به ثانیه (پیش‌فرض ۳۰۰ = ۵ دقیقه)
5. برو به تب **Settings** و مطمئن شو نوع سرویس روی **Worker** تنظیم شده
   (نه Web) — چون این برنامه سرور HTTP نداره
6. Deploy رو بزن. Railway خودش پکیج‌ها رو نصب می‌کنه و `bot.py` رو اجرا می‌کنه

از این به بعد، هر بار که کد رو توی گیت‌هاب push کنی، Railway خودکار
دوباره دیپلویش می‌کنه. اگه برنامه کرش کنه هم Railway خودش دوباره
ری‌استارتش می‌کنه.

## اجرای محلی (برای تست قبل از دیپلوی)

```bash
pip install -r requirements.txt
export BOT_TOKEN="توکن ربات"
export CHANNEL_ID="@your_channel"
python bot.py
```

## نکات

- Railway پلن رایگان (Trial/Hobby) داره ولی محدودیت ساعت اجرا و مصرف
  ماهانه داره — برای یه ربات سبک مثل این معمولاً کافیه، ولی بهتره خودت
  قیمت‌گذاری فعلی Railway رو چک کنی چون ممکنه تغییر کرده باشه.
- اگه API منبع (`bonbast.amirhn.com`) موقتاً در دسترس نبود، ربات خطا رو
  توی لاگ چاپ می‌کنه و ۵ دقیقه بعد دوباره امتحان می‌کنه؛ کرش نمی‌کنه.
