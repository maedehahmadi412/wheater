import requests
import datetime
city = input("لطفاً نام شهر رو وارد کن: ")
days_ahead = input(":برای چند روز آینده پیش‌بینی می‌خواهید؟ ")
try:
    days_ahead = int(days_ahead)
    if days_ahead < 1:
        print("لطفاً عدد بزرگتر یا مساوی 1 وارد کن.")
        exit()
except:
    print("لطفاً یک عدد معتبر وارد کن.")
    exit()
api_key = "5a0fd0be5f45c8b480529738a753f452"

def show_today_weather(city):
    url_today = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    try:
        response = requests.get(url_today)
        data = response.json()
        if data.get('cod') != 200:
            print("خطا در دریافت داده‌ها: ", data.get('message', 'داده پیدا نشد.'))
            return
        print("\n======== وضعیت هوای امروز ========")
        print(f"شهر: {data['name']}")
        print(f"دما: {data['main']['temp']} °C")
        print(f"رطوبت: {data['main']['humidity']}%")
        print(f"وضعیت کلی: {data['weather'][0]['description'].capitalize()}")
        print(f"سرعت باد: {data['wind']['speed']} متر/ثانیه")
        print("="*40)
    except Exception as e:
        print("خطا در دریافت وضعیت امروز:", e)

def show_forecast_for_days(city, days):
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    try:
        response = requests.get(forecast_url)
        data = response.json()

        if data.get('cod') != '200':
            print("خطا در دریافت پیش‌بینی: ", data.get('message', 'داده پیدا نشد.'))
            return

        target_date = (datetime.datetime.now() + datetime.timedelta(days=days)).date()
        forecasts = [
            entry for entry in data['list']
            if datetime.datetime.fromtimestamp(entry['dt']).date() == target_date
        ]

        if not forecasts:
            print(f"پیش‌بینی برای {days} روز بعد در دسترس نیست.")
            return

        print(f"\n======== پیش‌بینی در {days} روز آینده ========")
        for entry in forecasts:
            dt = datetime.datetime.fromtimestamp(entry['dt'])
            time_str = dt.strftime('%H:%M')
            temp = entry['main']['temp']
            humidity = entry['main']['humidity']
            wind_speed = entry['wind']['speed']
            description = entry['weather'][0]['description'].capitalize()

            print(f"ساعت: {time_str} | دما: {temp}°C | رطوبت: {humidity}% | باد: {wind_speed} متر/ثانیه | وضعیت: {description}")
        print("="*40)
    except Exception as e:
        print("خطا در دریافت پیش‌بینی:", e)
show_today_weather(city)
show_forecast_for_days(city, days_ahead)
