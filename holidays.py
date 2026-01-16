import requests
from bs4 import BeautifulSoup
from datetime import date
import logging

def get_today_holiday_calend():
    d = date.today()
    url = f"https://www.calend.ru/day/{d.year}-{d.month:02d}-{d.day:02d}/"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # Первый праздник дня
        #holiday = soup.select_one("ul.events li a")
        holidays = soup.select("div.holidays ul.itemsNet>li>div.caption>span.title")
        holiday = holidays[0].get_text(strip=True) if holidays else None
        if holiday:
            print(holiday.strip())
            return holiday.strip()

    except Exception as e:
        logging.error(f"calend error: {e}")

    return None

if __name__ == "__main__":
    get_today_holiday_calend()