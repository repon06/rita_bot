import logging
import time

import requests

from config import HOST_BOT

PING_INTERVAL = 40  # Интервал между пингами (в секундах)


def ping_server():
    """Функция для отправки пингов на сервер."""
    while True:
        try:
            response = requests.get(HOST_BOT)
            logging.debug(f"Пинг успешен: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Ошибка при пинге: {e}")
        time.sleep(PING_INTERVAL)

# Запустите пинг-цикл в отдельном потоке
# threading.Thread(target=ping_server, daemon=True).start()
