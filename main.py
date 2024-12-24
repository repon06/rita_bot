import asyncio
import json
import logging
import os
import threading

from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import TOKEN_TG, HOST_BOT
from handlers import start, reply_to_phrases
from scheduler import setup_scheduler
import ping  # Импортируем ping.py

app = Flask(__name__)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

application = None  # Глобальная ссылка на приложение


# Асинхронная функция для установки вебхука
async def set_webhook():
    """Устанавливаем вебхук для Telegram бота."""
    await application.bot.set_webhook(HOST_BOT + "/webhook")


async def setup_application(application):
    """Настраивает приложение, включая вебхук и планировщик."""
    await set_webhook()  # Устанавливаем вебхук
    setup_scheduler(application)  # Настройка планировщика


# Функция для запуска Telegram бота
def start_telegram_bot():
    global application
    application = ApplicationBuilder().token(TOKEN_TG).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, reply_to_phrases))

    # Получаем текущий событийный цикл
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_application(application))  # Настраиваем приложение

    # Запускаем сервер для пинга в отдельном потоке
    ping_thread = threading.Thread(target=ping.ping_server, daemon=True)
    ping_thread.start()

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(timeout=40, poll_interval=1)


# Flask endpoint для получения вебхуков
@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка запросов от Telegram через вебхук."""
    if request.method == 'POST':
        json_data = json.loads(request.get_data().decode('UTF-8'))
        update = Update.de_json(json_data, application.bot)
        application.update_queue.put(update)
        return 'OK'


@app.route('/')
def index():
    """Тестовая страница для проверки работы сервера."""
    return "Бот работает!"


# Функция для запуска Flask сервера
def start_flask():
    """Запуск Flask сервера."""
    port = int(os.environ.get("PORT", 5555))
    app.run(host='0.0.0.0', port=port, debug=False)


# Основная функция для запуска как Telegram бота, так и Flask сервера
def main():
    # Создаем событийный цикл, если его нет
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    # Запускаем Flask в отдельном потоке
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Запуск Telegram бота
    start_telegram_bot()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот остановлен.")