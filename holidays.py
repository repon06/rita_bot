import logging
import random
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
        holiday_list = soup.select("div.holidays ul.itemsNet>li>div.caption>span.title")
        holiday = holiday_list[0].get_text(strip=True) if holiday_list else None

        # знаменательные даты - блоки список "div.knownDates>ul>li"
        # знаменательные даты - блоки год "div.knownDates>ul>li span.year_on_img"
        # знаменательные даты - блоки описание "div.knownDates>ul>li span.title"
        known_dates_list = soup.select("div.knownDates>ul>li")
        item = random.choice(known_dates_list)
        holiday_year = item.select_one("span.year").get_text(strip=True)
        holiday_title = item.select_one("span.title a").get_text(strip=True)

        holiday = f'{holiday_year} {holiday_title}'

        if holiday:
            logging.info(holiday.strip())
            return holiday.strip()

    except Exception as e:
        logging.error(f"calend error: {e}")

    return None


if __name__ == "__main__":
    holiday = get_today_holiday()
