import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import TOKEN_TG


# Обработчик для текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Выводим текст в консоль, чтобы убедиться, что сообщение получено
    print(f"Received message: {update.message.text}")
    await update.message.reply_text(f"Вы СКАЗАЛИ: {update.message.text}")


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот Рита 🤖.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # Создаем приложение бота
    application = ApplicationBuilder().token(TOKEN_TG).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик всех текстовых сообщений (кроме команд)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Запуск бота
    application.run_polling()
