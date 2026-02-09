import os
from datetime import date

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ====== Загружаем переменные из .env ======
load_dotenv()  # теперь os.environ видит HF_TOKEN

# ====== Настройка клиента ======
client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"],  # теперь ключ точно есть
)


def generate(holiday_text=None):
    today = date.today().strftime("%d.%m.%Y")
    holiday_text = 'Всемирный день The Beatles'
    holiday_text = 'Татьянин день — День российского студенчества'

    prompt = (
        f"Poster for {holiday_text}, retro style, musical notes, "
        f"Сгенерируй открытку с стиле открыток СССР с изображением {holiday_text}, "
        f"iconic silhouettes of {holiday_text}, cheerful atmosphere, "
        f"text: '{holiday_text} {today}'"
    )

    # Генерация картинки
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev"
    )

    filename = "holidays.png"
    image.save(filename)

    print(f"Картинка сохранена как {filename}, дата: {today}")  # ASCII только


if __name__ == "__main__":
    generate()
