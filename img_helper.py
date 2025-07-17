import logging
from io import BytesIO

import requests
from PIL import Image

from config import ACCESS_KEY_UNSPLASH, HARVARD_ART_MUSEUMS_KEY

logger = logging.getLogger(__name__)


def get_random_url_image(width=1080):
    response = requests.get(
        f'https://api.unsplash.com/photos/random?query=winter+nature+animals+bright&client_id={ACCESS_KEY_UNSPLASH}'
    )

    if response.status_code == 200:
        image_url = response.json()['urls']['regular']
        return f"{image_url}&w={width}"
    else:
        return None


def get_img_data_by_url(image_url: str):
    if image_url:
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                if img_data:
                    resized_data = resize_image(img_data, width=1080)
                    if resized_data:
                        with open("resized.jpg", "wb") as f:
                            f.write(resized_data.read())
                return resized_data
            else:
                logger.error(f"Не удалось загрузить картинку. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке изображения: {e}")
    return None


def resize_image(image_data: BytesIO, width: int) -> BytesIO | None:
    try:
        img = Image.open(image_data)
        w_percent = width / float(img.size[0])
        height = int((float(img.size[1]) * float(w_percent)))
        resized_img = img.resize((width, height), Image.Resampling.LANCZOS)

        output = BytesIO()
        resized_img.save(output, format="JPEG")
        output.seek(0)
        return output
    except Exception as e:
        logger.error(f"Ошибка при ресайзе изображения: {e}")
        return None


def get_harvard_art(width=1080, max_attempts=10):
    api_key = HARVARD_ART_MUSEUMS_KEY
    base_url = "https://api.harvardartmuseums.org/object"
    query = 'verificationlevel:4 AND classification:Paintings AND peoplecount:1 AND primaryimageurl:*'

    for _ in range(max_attempts):
        resp = requests.get(base_url, params={
            "apikey": api_key,
            "size": 1,
            "hasimage": 1,
            "sort": "random",
            "q": query,
            "fields": "title,people,description,primaryimageurl"
        }).json()

        records = resp.get("records", [])
        if not records:
            continue

        record = records[0]
        image_url = record.get("primaryimageurl")
        if not image_url:
            continue

        return {
            "title": record.get("title"),
            "artist": record.get("people", [{}])[0].get("name"),
            "description": record.get("description"),
            "image": f"{image_url}?width={width}"
        }

    return None


def get_met_art(width=1080):
    # Step 1: Поиск объектов с известным художником
    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {
        "q": "Van Gogh",
        "hasImages": "true",
        "artistOrCulture": "true"
    }
    search = requests.get(search_url, params=params).json()
    object_ids = search.get("objectIDs", [])

    if not object_ids:
        return None

    # Step 2: Получение информации о первом объекте
    object_id = object_ids[0]
    object_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    obj_data = requests.get(object_url).json()

    image_url = obj_data.get("primaryImage")

    # The MET не поддерживает параметр width, поэтому обрабатываем локально или используем resize-сервис
    if image_url:
        resized_image = f"{image_url}?width={width}"  # можно через прокси или внешний ресайзер

        return {
            "title": obj_data.get("title"),
            "artist": obj_data.get("artistDisplayName"),
            "description": obj_data.get("creditLine"),
            "image": resized_image
        }


if __name__ == "__main__":
    print(get_met_art())
    print(get_harvard_art())
