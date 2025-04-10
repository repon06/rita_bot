from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_TG = os.getenv("TOKEN_TG")
ACCESS_KEY_UNSPLASH = os.getenv("ACCESS_KEY_UNSPLASH")
# CHAT_ID = "-1002334608878"  # Укажите ID - test_group
CHAT_ID = -1002465540172  # Chat ID Мысникова6

PHONE_AVARIA_UK = '759-659'
PHONE_UPRAV_UK = '+79372255507'
PHONE_SARATOV_VODOKANAL = '32-00-00'
PHONE_DISPECHER = '659-659'
PHONE_LIFT = '695-424'
PHONE_T_PLUS = '32-00-22'
PHONE_DISPECHER_KIROVSKIY = '659-872'
PHONE_AO_SPGES = '8 (800) 775-57-89'
GAS_URL = 'мойгаз.смородина.онлайн'

DAYS = [10, 15, 19]  # Дни месяца для напоминаний

HOST_BOT = 'https://rita-bot.onrender.com' # URL хостинга на Render

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_CITY = 'Saratov'
WEATHER_COUNTRY = 'RU'