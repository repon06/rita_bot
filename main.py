import asyncio
import logging

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram.ext import CommandHandler

from config import TOKEN_TG, CHAT_ID, ACCESS_KEY_UNSPLASH

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Сохраняем ссылку на application для последующего использования
application = None


async def send_morning_image(context):
    """Отправляет картинку с текстом каждое утро."""
    image_url = get_images()
    if image_url:
        await context.send_photo(
            chat_id=CHAT_ID,
            photo=image_url,
            caption="Доброе утро! 🌞\nНе забудьте улыбнуться сегодня!\nУК помнит о Вас)",
        )
    else:
        logger.error("Не удалось отправить утреннюю картинку: URL не найден.")


async def handle_fix_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Для уточнения вопроса звоните по номеру: 759659")


# === 2. Функция для отправки напоминания 10 числа ===
async def send_monthly_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Напоминание о передаче показаний счетчиков каждое 10 число."""
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="📅 Сегодня 10-е число! Не забудьте передать показания счетчиков!",
    )


# === 3. Ответы на сообщения пользователей ===
async def reply_to_phrases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на фразы 'куда звонить' и 'когда починят?'."""
    user_message = update.message.text.lower()  # Приводим к нижнему регистру
    if "куда звонить" in user_message or "когда починят" in user_message:
        await update.message.reply_text(
            "Для решения вопросов звоните по телефону 📞 759659"
        )


# === 4. Функция для старта бота ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот Рита 🤖. Могу:\n"
        "- Присылать утренние напоминания 🌅\n"
        "- Напоминать 10-го числа передавать показания 📊\n"
        "- Отвечать на вопросы, куда следует звонить."
    )


def setup_scheduler(application):
    """Настройка планировщика для выполнения задач."""
    scheduler = BackgroundScheduler(timezone="Europe/Saratov")

    # Задача для утреннего сообщения
    scheduler.add_job(
        lambda: asyncio.run(send_morning_image(application.bot)),
        trigger="cron",
        hour=11,
        minute=17,
    )

    # Задача для напоминания 10 числа
    scheduler.add_job(
        lambda: asyncio.run(send_monthly_reminder(application.bot)),
        trigger="cron",
        day=10,
        hour=9,
        minute=0,
    )

    scheduler.start()


# === Основной запуск бота ===
def main():
    global application  # Объявляем переменную глобальной
    # Создаем приложение бота
    application = ApplicationBuilder().token(TOKEN_TG).build()

    # Обработчики
    application.add_handler(CommandHandler("start", start))

    # Обработчик сообщений, который реагирует на фразы с учетом регистра
    application.add_handler(MessageHandler(
        filters.Regex(r'(?i).*отопление.*когда.*починят\?.*'),  # Убедитесь, что фраза отслеживается
        handle_fix_request
    ))

    # Обработчик текстовых сообщений, который отвечает на "куда звонить" или "когда починят"
    application.add_handler(
        MessageHandler(filters.TEXT, reply_to_phrases)
        # MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_phrases)
    )

    # Настройка планировщика
    setup_scheduler(application)

    # Запуск бота
    logger.info("Бот запущен...")
    application.run_polling()


def get_images(width=1080):
    response = requests.get(
        f'https://api.unsplash.com/photos/random?query=winter+nature+animals+bright&client_id={ACCESS_KEY_UNSPLASH}'
    )

    # Проверка успешности запроса
    if response.status_code == 200:
        image_url = response.json()['urls']['regular']
        # Добавляем параметр ширины
        return f"{image_url}&w={width}"
    else:
        logger.error("Ошибка при запросе изображения от Unsplash")
        return None


async def shutdown():
    global application
    await application.shutdown()
    await application.stop()
    await application.wait_closed()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        asyncio.run(shutdown())
