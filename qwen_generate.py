import asyncio
import requests
from pathlib import Path
from playwright.async_api import async_playwright

from config import EMAIL, PASSWORD, BASE_DIR

generate_image_path = BASE_DIR / "img" / "generate_image.png"

async def generate_poster_holiday(holiday: str):
    query_text = (
        f"Создай краткий и емкий промт на английском языке для генерации постера открытки "
        f"с соотношением сторон: 9:16 для события: '{holiday}'."
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-notifications"
        ])
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://chat.qwen.ai/auth")

        # Ввод логина и пароля
        await page.fill("input[name='email']", EMAIL)
        await page.fill("input[name='password']", PASSWORD)
        await page.click("button.qwenchat-auth-pc-submit-button.brandprimary")

        # Ждём загрузки чата
        await page.wait_for_selector("div.placeholder-logo-text")

        # Вводим запрос
        await page.fill("textarea.chat-input", query_text)
        await page.click("button.send-button")

        # Ждём окончания генерации текста
        await page.wait_for_selector("div.qwen-message-content-text", timeout=300000)  # до 5 мин
        result_text = await page.inner_text("div.qwen-message-content-text")
        print("Промт:", result_text)

        # Переходим к генерации изображения
        await page.click("//div[text()='Image Generation' or text()='Генерация изображений']")
        await page.fill("textarea.chat-input", result_text)
        await page.click("button.send-button")

        # Ждём, пока изображение появится
        img_element = await page.wait_for_selector("img.ant-image-img", timeout=600000)  # до 10 мин
        img_url = await img_element.get_attribute("src")

        # Скачиваем изображение напрямую
        r = requests.get(img_url, timeout=30)
        r.raise_for_status()
        generate_image_path.parent.mkdir(parents=True, exist_ok=True)
        with open(generate_image_path, "wb") as f:
            f.write(r.content)

        await browser.close()
        return generate_image_path

if __name__ == "__main__":
    asyncio.run(generate_poster_holiday("Международный день ювелира"))