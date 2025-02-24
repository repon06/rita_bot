import requests

from config import WEATHER_CITY, WEATHER_COUNTRY, WEATHER_API_KEY


def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY},{WEATHER_COUNTRY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"Сейчас в Саратове {temp}°C, {weather_desc}"
    else:
        return "Не удалось получить данные о погоде."