import logging
from io import BytesIO

import requests

from config import ACCESS_KEY_UNSPLASH

logger = logging.getLogger(__name__)


def get_images(width=1080):
    response = requests.get(
        f'https://api.unsplash.com/photos/random?query=winter+nature+animals+bright&client_id={ACCESS_KEY_UNSPLASH}'
    )

    # Проверка успешности запроса
    if response.status_code == 200:
        image_url = response.json()['urls']['regular']
        # Добавляем параметр ширины
        return f"{image_url}&w={width}"
    else:
        return None


def get_img_data_by_url(image_url: str):
    if image_url:
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                return BytesIO(response.content)
            else:
                logger.error(f"Не удалось загрузить картинку. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке изображения: {e}")
    return None
