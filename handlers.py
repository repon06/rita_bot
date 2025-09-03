import datetime
import logging
from pathlib import Path

from cachetools import TTLCache
from telegram import Update
from telegram.ext import ContextTypes

from config import PHONE_SARATOV_VODOKANAL, PHONE_T_PLUS, PHONE_AVARIA_UK, PHONE_LIFT, PHONE_DISPECHER_KIROVSKIY, \
    PHONE_DISPECHER, PHONE_AO_SPGES, PHONE_UPRAV_UK, CHAT_ID, GAS_URL, AD_KEYWORDS
from img_helper import get_random_url_image, get_img_data_by_url
from weather import get_weather

logger = logging.getLogger(__name__)

# Кеш на 30 минут: max 1000 записей
message_cache = TTLCache(maxsize=1000, ttl=30 * 60)


def is_on_cooldown_global(chat_id: int, key: str) -> bool:
    cache_key = (chat_id, key)
    if cache_key in message_cache:
        return True
    message_cache[cache_key] = True
    return False


async def reply_to_phrases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_message = update.message.text.lower().strip()
    if not user_message:
        return

    if ("куда звонить" in user_message or "когда починят" in user_message):
        if not is_on_cooldown_global(chat_id, "repair_info"):
            await update.message.reply_text(f"Для решения вопросов звоните по телефону 📞\n"
                                            f"Аварийно-диспетчерская служба управляющей компании (круглосуточно): {PHONE_AVARIA_UK}")

    elif any(word in user_message for word in ["вода", "водой", "воды", "отопление"]):
        if not is_on_cooldown_global(chat_id, "water_info"):
            await update.message.reply_text(f"Для решения вопросов звоните по телефону 📞:\n"
                                            f"Аварийно-диспетчерская служба управляющей компании (круглосуточно): {PHONE_AVARIA_UK}\n"
                                            f"Саратовводоканал: {PHONE_SARATOV_VODOKANAL}\n"
                                            f"Т Плюс: {PHONE_T_PLUS}")

    elif "лифт" in user_message:
        if not is_on_cooldown_global(chat_id, "lift_info"):
            await update.message.reply_text(f"Для решения вопросов звоните по телефону 📞\n"
                                            f"Аварийная служба лифтовиков: {PHONE_LIFT}")

    elif "индекс" in user_message:
        if not is_on_cooldown_global(chat_id, "zip_info"):
            await update.message.reply_text("Почтовый индекс нашего дома: 410082")

    elif any(word in user_message for word in [" рита", " рите", " риту"]):
        if not is_on_cooldown_global(chat_id, "rita_intro"):
            await update.message.reply_text("Привет! Я бот Рита 🤖. Могу:\n"
                                            "- Присылать утренние напоминания 🌅\n"
                                            "- Напоминать передавать показания счетчиков 📊\n"
                                            "- Отвечать на вопросы, куда следует звонить.")

    elif "паспортист" in user_message or "офис ук" in user_message:
        if not is_on_cooldown_global(chat_id, "office_info"):
            await update.message.reply_text("Уважаемые собственники!\n"
                                            "Офис управляющей компании переехал, теперь находится по адресу: г.Саратов, ул. Им. Тархова д. 45а, кв. 99, этаж 1, домофон № 99.\n"
                                            "Режим работы офиса - с 9:00 до 18:00.\n"
                                            "Режим работы паспортного стола остался такой же.\n"
                                            "Пн. С 14:00 до 18:00\n"
                                            "Чт. С 9:00 до 11:00")

    elif "свет" in user_message or "электричеств" in user_message:
        if not is_on_cooldown_global(chat_id, "electric_info"):
            await update.message.reply_text(
                f"Уточнить информацию о перебоях (отключении) тепло-, водо-, электро- и газоснабжения можно по следующим телефонам 📞:\n"
                f"Диспетчерский пункт по Кировскому району: {PHONE_DISPECHER_KIROVSKIY}\n"
                f"Центральный диспетчерский пункт: {PHONE_DISPECHER}\n"
                f"Горячая линия АО СПГЭС: {PHONE_AO_SPGES}\n"
                f"Т Плюс: {PHONE_T_PLUS}")

    elif any(word in user_message for word in ["управляющая компания", "управляющей компании",
                                               "адрес ук", "адрес нашей ук", "управляющую компанию",
                                               "сергей федорович"]):
        if not is_on_cooldown_global(chat_id, "uk_info"):
            await update.message.reply_text(f"Уважаемые собственники!\n"
                                            "Офис управляющей компании переехал, теперь находится по адресу: г.Саратов, ул. Им. Тархова д. 45а, кв. 99, этаж 1, домофон № 99.\n"
                                            f"Управляющий УК Сергей Федорович: {PHONE_UPRAV_UK}")
    elif any(word in user_message for word in
             ["тишина", "тишину", "топот", "топание", "топонье", "шум", "сверли", "сверлен", "досверл"]):
        if not is_on_cooldown_global(chat_id, "silent"):
            await update.message.reply_text(
                'Закон Саратовской области от 2 декабря 2020 года № 148‑ЗСО "Об обеспечении тишины и покоя граждан на территории Саратовской области"\r\n'
                'Закон Саратовской области от 3 июля 2024 года № 80-ЗСО "О внесении изменений в некоторые законодательные акты Саратовской области"'
            )
    elif "погода" in user_message or "погоду" in user_message:
        if not is_on_cooldown_global(chat_id, "weather_info"):
            weather_info = get_weather()
            await update.message.reply_text(weather_info)
    elif "правила" in user_message or "правила чата" in user_message:
        if not is_on_cooldown_global(chat_id, "rules_info"):
            await update.message.reply_text(
                "<b>Первое правило</b>: Не упоминать о Чате Мысникова 6.\n"
                "<b>Второе правило</b>: Не упоминать нигде о Чате Мысникова 6.\n"
                "<b>Третье правило</b>: Никакой рекламы! Для этого есть соответствующие площадки.",
                parse_mode="HTML")

    elif any(phrase in user_message for phrase in
             ["показания газ", "газовые показания", "показания по газу", "данные по газу"]):
        if not is_on_cooldown_global(chat_id, "gas_info"):
            await update.message.reply_text(
                "Показания счетчиков газа можно передать в Приложении или на сайте 'мой газ'.\n"
                f"{GAS_URL}")
    elif any(phrase in user_message for phrase in ["тестовая картинка"]):
        image_url = get_random_url_image()
        image_data = get_img_data_by_url(image_url)
        await update.message.reply_text("тестовая картинка")

        if image_url:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_data,
                caption="тестовая картинка"
            )
    elif "3 сентября" in user_message:
        today = datetime.date.today().strftime("%d/%m")
        BASE_DIR = Path(__file__).resolve().parent
        img_path = BASE_DIR / "img" / "3_sent_2.jpeg"
        await update.message.reply_text(
            f"я календарь переверну...\r\n{today}\r\npath exist: {img_path.exists()}", parse_mode="HTML")
        if today == "03/09":
            if img_path.exists():
                with img_path.open("rb") as photo:
                    await context.bot.send_photo(
                        chat_id=CHAT_ID,
                        photo=photo,
                        caption=f"Не забудьте календарь перевернуть!",
                    )
    elif any(word in user_message for word in AD_KEYWORDS):
        logger.warning(f"SPAM: Рекламное сообщение '{update.message.text}' удалено.")
        await update.message.delete()


async def send_morning_image(bot):
    """Отправляет картинку с текстом каждое утро."""
    weather_info = get_weather()

    today = datetime.date.today().strftime("%d/%m")
    if today == "03/09":
        # отправляем локальный файл
        img_path = Path("img/3_sent_2.jpeg")
        if img_path.exists():
            with img_path.open("rb") as photo:
                await bot.send_photo(
                    chat_id=CHAT_ID,
                    photo=photo,
                    caption=f"Доброе утро! 🌞\nНе забудьте календарь перевернуть!\n{weather_info}",
                )
    else:
        image_url = get_random_url_image()
        if image_url:
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=image_url,
                caption=f"Доброе утро! 🌞\nНе забудьте сегодня улыбнуться!\n{weather_info}",
            )
        else:
            logger.error("Не удалось отправить утреннюю картинку: URL не найден.")


async def send_monthly_reminder(bot, message: str):
    """Напоминание о передаче показаний счетчиков."""
    await bot.send_message(
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
