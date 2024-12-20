import asyncio
import json
import logging
import os
import threading

from flask import Flask, request
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram.ext import CommandHandler

from config import TOKEN_TG, HOST_BOT
from handlers import start, reply_to_phrases
from scheduler import setup_scheduler

import ping  # Импортируем ping.py
app = Flask(__name__)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

application = None  # Ссылка на приложение, чтобы можно было остановить его в случае ошибки


# Асинхронная функция для установки вебхука
async def set_webhook():
    await application.bot.set_webhook(HOST_BOT + "/webhook")


# Асинхронная обработка ошибок, включая завершение работы бота
async def handle_shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок, который завершает бота."""
    logger.error(f"Произошла ошибка: {context.error}")
    if isinstance(context.error, NetworkError):
        if application:
            await application.shutdown()  # правильное использование await
        else:
            logger.error("Ошибка: приложение не инициализировано.")
    else:
        raise context.error


# Функция для инициализации Telegram бота
def start_telegram_bot():
    global application  # Объявляем переменную глобальной
    application = ApplicationBuilder().token(TOKEN_TG).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, reply_to_phrases))
    application.add_error_handler(handle_shutdown)  # для безопасного завершения работы приложения

    setup_scheduler(application)  # Настройка планировщика

    # Запуск вебхука асинхронно
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())

    # Запускаем сервер для пинга
    ping_thread = threading.Thread(target=ping.ping_server, daemon=True)
    ping_thread.start()  # Запускаем пинг в отдельном потоке

    # Запуск бота
    logger.info("Бот запущен...")
    application.run_polling(timeout=40, poll_interval=1)


# Flask endpoint для получения вебхуков
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        json_str = request.get_data().decode('UTF-8')  # Получаем строку
        json_data = json.loads(json_str)  # Преобразуем строку JSON в словарь
        update = Update.de_json(json_data, application.bot)  # Передаем словарь
        application.update_queue.put(update)
        return 'OK'


@app.route('/')
def index():
    return "Бот работает!"


# Запуск Flask в отдельном потоке
def start_flask():
    # Настроить порт для Flask
    port = int(os.environ.get("PORT", 5555))  # Render автоматически назначит порт
    app.run(host='0.0.0.0', port=port, debug=False)  # Запуск Flask на порту, который назначает Render


# Основная функция для запуска как Telegram бота, так и Flask сервера
def main():
    # Запуск Flask в отдельном потоке
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    # Запуск Telegram бота
    start_telegram_bot()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот завершил работу по команде остановки.")
