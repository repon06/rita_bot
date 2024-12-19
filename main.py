import asyncio
import logging

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram.ext import CommandHandler

from config import TOKEN_TG, CHAT_ID, ACCESS_KEY_UNSPLASH, PHONE_AVARIA_UK, PHONE_SARATOV_VODOKANAL, PHONE_LIFT, \
    PHONE_T_PLUS, PHONE_UPRAV_UK, PHONE_DISPECHER_KIROVSKIY, PHONE_DISPECHER, PHONE_AO_SPGES, DAYS

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

application = None  # Ссылка на приложение, чтобы можно было остановить его в случае ошибки


async def debug_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Text received in group: {update.message.text}")
    print(f"Message received: {update.message.text}")
    await update.message.reply_text("Сообщение получено!")


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
    await update.message.reply_text(f"Для уточнения вопроса звоните по номеру: {PHONE_AVARIA_UK}")


# === 2. Функция для отправки напоминания 10 числа ===
async def send_monthly_reminder(context: ContextTypes.DEFAULT_TYPE, message: str):
    """Напоминание о передаче показаний счетчиков."""
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=message,
    )


# === 3. Ответы на сообщения пользователей ===
async def reply_to_phrases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received message: {update.message.text}")
    user_message = update.message.text.lower().strip()
    if not user_message:
        return  # Игнорируем пустые сообщения
    if "куда звонить" in user_message or "когда починят" in user_message:
        await update.message.reply_text(f"Для решения вопросов звоните по телефону 📞\n"
                                        f"Аварийно-диспетчерская служба управляющей компании (круглосуточно): {PHONE_AVARIA_UK}")
    elif "вода" in user_message or "воды" in user_message or "отопление" in user_message:
        await update.message.reply_text(f"Для решения вопросов звоните по телефону 📞:\n"
                                        f"Аварийно-диспетчерская служба управляющей компании (круглосуточно): {PHONE_AVARIA_UK}\n"
                                        f"Саратовводоканал: {PHONE_SARATOV_VODOKANAL}\n"
                                        f"Т Плюс: {PHONE_T_PLUS}")
    elif "лифт" in user_message:
        await update.message.reply_text(f"Для решения вопросов звоните по телефону 📞\n"
                                        f"Аварийная служба лифтовиков: {PHONE_LIFT}")
    elif "индекс" in user_message:
        await update.message.reply_text("Почтовый индекс нашего дома: 410082")
    elif " рита" in user_message or " рите" in user_message or " риту" in user_message:
        await update.message.reply_text("Привет! Я бот Рита 🤖. Могу:\n"
                                        "- Присылать утренние напоминания 🌅\n"
                                        "- Напоминать 10-15-20-го числа передавать показания счетчиков 📊\n"
                                        "- Отвечать на вопросы, куда следует звонить.")
    elif "паспортист" in user_message or "офис ук" in user_message:
        await update.message.reply_text("Уважаемые собственники!\n"
                                        "Офис управляющей компании переехал, теперь находится по адресу: г.Саратов, ул. Им. Тархова д. 45а, кв. 99, этаж 1, домофон № 99.\n"
                                        "Режим работы офиса - с 9:00 до 18:00.\n"
                                        "Режим работы паспортного стола остался такой же.\n"
                                        "Пн. С 14:00 до 18:00\n"
                                        "Чт. С 9:00 до 11:00")
    elif "свет" in user_message or "электричеств" in user_message:
        await update.message.reply_text(
            f"Уточнить информацию о перебоях (отключении) тепло-, водо-, электро- и газоснабжения можно по следующим телефонам 📞:\n"
            f"Диспетчерский пункт по Кировскому району: {PHONE_DISPECHER_KIROVSKIY}\n"
            f"Центральный диспетчерский пункт: {PHONE_DISPECHER}\n"
            f"Горячая линия АО СПГЭС: {PHONE_AO_SPGES}\n"
            f"Т Плюс: {PHONE_T_PLUS}")
    if ("управляющая компания" in user_message or "управляющей компании" in user_message
        or "управляющую компанию" in user_message) or "Сергей Федорович" in user_message:
        await update.message.reply_text(f"Уважаемые собственники!\n"
                                        "Офис управляющей компании переехал, теперь находится по адресу: г.Саратов, ул. Им. Тархова д. 45а, кв. 99, этаж 1, домофон № 99.\n"
                                        f"Управляющий УК Сергей Федорович: {PHONE_UPRAV_UK}")


# === 4. Функция для старта бота ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот Рита 🤖. Могу:\n"
        "- Присылать утренние напоминания 🌅\n"
        "- Напоминать 10-15-20-го числа передавать показания счетчиков 📊\n"
        "- Отвечать на вопросы, куда следует звонить."
    )


def setup_scheduler(application):
    """Настройка планировщика для выполнения задач."""
    scheduler = BackgroundScheduler(timezone="Europe/Saratov")

    # Задача для утреннего сообщения
    scheduler.add_job(
        lambda: asyncio.run(send_morning_image(application.bot)),
        trigger="cron",
        hour=9,
        minute=00,
    )

    for day in DAYS:
        scheduler.add_job(
            lambda: asyncio.run(
                send_monthly_reminder(application.bot,
                                      f"📅 Сегодня {day}-е число! Не забудьте передать показания счетчиков!")
            ),
            trigger="cron",
            day=day,
            hour=9,
            minute=5,
        )

    scheduler.start()


# === Основной запуск бота ===
def main():
    global application  # Объявляем переменную глобальной

    application = ApplicationBuilder().token(TOKEN_TG).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, reply_to_phrases))
    # application.add_handler(MessageHandler(filters.ALL, debug_messages))

    # Настройка планировщика
    setup_scheduler(application)

    # Запуск бота
    logger.info("Бот запущен...")
    # application.run_polling() # кажд 10 сек
    application.run_polling(timeout=60)

    # Используем обработчик завершения работы для безопасного завершения работы приложения
    application.add_error_handler(handle_shutdown)


async def handle_shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок, который завершает бота."""
    logger.error(f"Произошла ошибка: {context.error}")
    if isinstance(context.error, NetworkError):
        await application.stop()
        await application.wait_closed()
    else:
        raise context.error


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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот завершил работу по команде остановки.")
