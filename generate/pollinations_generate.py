import http.client
import logging
import urllib
import urllib.parse

import holidays
from config import POLLINATIONS_REPON_KEY, BASE_DIR

logger = logging.getLogger(__name__)
headers = {
    'Accept': "*/*",
    'Authorization': f"Bearer {POLLINATIONS_REPON_KEY}"}


def pollinations_generate_prompt(holiday: str):
    conn = None
    query_text = ("Создай краткий и емкий промпт на английском языке для генерации постера открытки "
                  "с соотношением сторон: 9:16 "
                  "к знаменательному событию в истории: "
                  f"'{holiday}'. "
                  # "Используй 5 цветов. Выведи в виде кода. ничего больше кроме промпта не выводи")
                  "Стиль cinematic realism, AI photography, bokeh depth shot, storytelling image, realistic creative AI generation, moody cinematic visual, viral AI post, travel inspired realism, AI storytelling composition, 8k, ultra detailed, sharp subject, soft background.. "
                  "Выведи в виде кода. ничего больше кроме промпта не выводи")
    logging.info(f'Запускаем запрос на генерацию промпта: {query_text}')

    encoded_query = urllib.parse.quote(query_text)
    try:
        conn = http.client.HTTPSConnection("gen.pollinations.ai")
        conn.request("GET", f"/text/{encoded_query}?&model=qwen-coder", headers=headers)
        res = conn.getresponse()
        data = res.read()
        result_prompt = data.decode("utf-8")
        logging.info(result_prompt)
        return result_prompt
    except Exception as e:
        logging.error(f'Ошибка при генерации промпта: {e}')
        return None
    finally:
        if conn:
            conn.close()


def pollinations_generate_poster(prompt: str):
    conn = None
    path = (BASE_DIR / "img" / "generate.png")
    encoded_query = urllib.parse.quote(prompt)
    logging.info(f'Запускаем запрос на генерацию изображения: {prompt}')

    try:
        conn = http.client.HTTPSConnection("gen.pollinations.ai")
        conn.request("GET",
                     f"/image/{encoded_query}?&model=zimage&width=450&height=800&seed=42&quality=high&aspectRatio=9:16",
                     headers=headers)
        res = conn.getresponse()
        data = res.read()

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)

        logging.info(f"Poster saved at: {path}")
        return path
    except http.client.HTTPException as e:
        logging.error(f'Ошибка при генерации картинки: {e}')
        return None
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    max_retries = 3
    holiday = holidays.get_today_holiday()
    print(holiday)
    holiday_prompt = pollinations_generate_prompt(holiday)
    print(holiday_prompt)
    # path = pollinations_generate_poster(prompt)

    for attempt in range(1, max_retries + 1):
        img_holiday_path = pollinations_generate_poster(holiday_prompt)

        if img_holiday_path and img_holiday_path.exists():
            break

        logger.warning(f"Попытка {attempt} не удалась, img_holiday_path={img_holiday_path}")
