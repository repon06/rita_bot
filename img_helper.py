import requests

from config import ACCESS_KEY_UNSPLASH


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
