import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

from config import DAYS
from handlers import send_morning_image, send_monthly_reminder


def setup_scheduler(application):
    """Настройка планировщика для выполнения задач."""
    scheduler = BackgroundScheduler(timezone="Europe/Saratov")

    # Задача для утреннего сообщения
    scheduler.add_job(
        lambda: asyncio.run(send_morning_image(application.bot)),
        trigger="cron",
        hour=9,
        minute=00)

    for day in DAYS:
        scheduler.add_job(
            lambda: asyncio.run(
                send_monthly_reminder(
                    application.bot, f"📅 Сегодня {day}-е число! Не забудьте передать показания счетчиков!")
            ),
            trigger="cron",
            day=day,
            hour=9,
            minute=5)

    scheduler.start()
