import logging

from telegram import Update
from telegram.ext import ContextTypes

from config import PHONE_SARATOV_VODOKANAL, PHONE_T_PLUS, PHONE_AVARIA_UK, PHONE_LIFT, PHONE_DISPECHER_KIROVSKIY, \
    PHONE_DISPECHER, PHONE_AO_SPGES, PHONE_UPRAV_UK, CHAT_ID
from img_helper import get_images

logger = logging.getLogger(__name__)


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
                                        "- Напоминать передавать показания счетчиков 📊\n"
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


async def send_monthly_reminder(context: ContextTypes.DEFAULT_TYPE, message: str):
    """Напоминание о передаче показаний счетчиков."""
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот Рита 🤖. Могу:\n"
        "- Присылать утренние напоминания 🌅\n"
        "- Напоминать передавать показания счетчиков 📊\n"
        "- Отвечать на вопросы, куда следует звонить."
    )


async def handle_fix_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Для уточнения вопроса звоните по номеру: {PHONE_AVARIA_UK}")


async def debug_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Text received in group: {update.message.text}")
    print(f"Message received: {update.message.text}")
    await update.message.reply_text("Сообщение получено!")
