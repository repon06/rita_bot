from telegram import Bot

from config import TOKEN_TG


async def check_bot_status():
    bot = Bot(token=TOKEN_TG)
    try:
        bot_info = await bot.get_me()
        print(f"Бот работает: {bot_info.first_name}")
    except Exception as e:
        print(f"Ошибка подключения к Telegram: {e}")


if __name__ == "__main__":
    check_bot_status()
 # curl https://api.telegram.org/bot<your-token>/getMe
 # curl https://api.telegram.org/bot<your-token>/getWebhookInfo
 # curl https://api.telegram.org/bot<your-token>/setWebhook?url=<your-server-url>
 # curl https://api.telegram.org/bot<your-token>/deleteWebhook