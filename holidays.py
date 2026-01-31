import logging
from datetime import date

import requests
from bs4 import BeautifulSoup


def get_today_holiday():
    d = date.today()
    url = f"https://www.calend.ru/day/{d.year}-{d.month:02d}-{d.day:02d}/"
    # url = f"https://www.calend.ru/day/2026-01-31/"
    logging.info(f'Ушел запрос {url}')
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # Первый праздник дня
        # holiday = soup.select_one("ul.events li a")
        holidays = soup.select("div.holidays ul.itemsNet>li>div.caption>span.title")
        holiday = holidays[0].get_text(strip=True) if holidays else None
        if holiday:
            print(holiday.strip())
            return holiday.strip()

    except Exception as e:
        logging.error(f"calend error: {e}")

    return None


if __name__ == "__main__":
    holiday = get_today_holiday()
