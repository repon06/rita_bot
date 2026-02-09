import io

from PIL import Image
from google import genai
from google.genai import types

from config import GEMINI_API_KEY


def generate_lite():
    import requests

    prompt = 'Dynamic Olympic luge poster: athlete speeding down icy track at sunset, motion blur trails, snow spray frozen in air, Olympic rings glowing above alpine peaks, 1964 Innsbruck vintage style, bold typography "Luge Debut 1964", crisp winter atmosphere'
    #url = f"https://image.pollinations.ai/prompt/{prompt}?width=450&height=800&model=flux"
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=450&height=800&model=zimage"

    response = requests.get(url)
    with open("poster.png", "wb") as f:
        f.write(response.content)
    print("Готово!")


def generate_poster():
    """
    только в платном аккаунте?
    :return:
    """
    client = genai.Client(api_key=GEMINI_API_KEY)

    print("Доступные модели для генерации изображений:")
    for model in client.models.list():
        # В новых версиях используем supported_actions
        print(model.name)
        print(f' {model.supported_actions}')
        if 'generate_images' in model.supported_actions or 'generateImages' in model.supported_actions:
            print(f"Имя для кода: {model.name}")

    response = client.models.generate_images(
        # ИСПРАВЛЕНО: Используем модель Imagen, а не Gemini
        model="imagen-4.0-generate-001",
        prompt="""
        Vertical cyberpunk advertising poster, 2:3.
        A cosmic cat drinking neon milk.
        Digital illustration, vibrant colors.
        Text "NEON CAT" on top, "Space Milk Edition" at bottom.
        """,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="9:16",
            output_mime_type="image/png"
        )
    )

    # Добавим проверку на случай блокировки промпта фильтрами безопасности
    if response.generated_images:
        img = response.generated_images[0]
        image = Image.open(io.BytesIO(img.image.image_bytes))
        image.save("poster.png")
        print("OK: Poster saved as poster.png")
    else:
        print("Error: No images generated. Check safety settings or prompt.")


if __name__ == "__main__":
    generate_lite()
    # generate_poster()
