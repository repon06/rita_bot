import http.client
import logging
import urllib
import urllib.parse

from config import POLLINATIONS_REPON_KEY, BASE_DIR

conn = http.client.HTTPSConnection("gen.pollinations.ai")
headers = {'Authorization': f"Bearer {POLLINATIONS_REPON_KEY}"}


def pollinations_generate_prompt(holiday: str):
    query_text = ("Создай краткий и емкий промпт на английском языке для генерации постера открытки "
                  "с соотношением сторон: 9:16 "
                  "к знаменательному событию в истории: "
                  f"'{holiday}'. "
                  "Используй 5 цветов. Выведи в виде кода. ничего больше кроме промпта не выводи")
    logging.info(f'Запускаем запрос на генерацию промпта: {query_text}')

    encoded_query = urllib.parse.quote(query_text)

    conn.request("GET", f"/text/{encoded_query}?&model=qwen-coder", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result_prompt = data.decode("utf-8")
    logging.info(result_prompt)
    return result_prompt


def pollinations_generate_poster(prompt: str):
    path = (BASE_DIR / "img" / "generate.png")
    encoded_query = urllib.parse.quote(prompt)
    logging.info(f'Запускаем запрос на генерацию изображения: {prompt}')

    try:
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
        logging.error(e)
        return None


if __name__ == "__main__":
    prompt = pollinations_generate_prompt("1969 Состоялся первый полет самолета Боинг 747")
    path = pollinations_generate_poster(prompt)
