import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import DAYS
from handlers import send_morning_image, send_monthly_reminder

def setup_scheduler(application):
    """Настройка планировщика для выполнения задач."""
    scheduler = AsyncIOScheduler(timezone="Europe/Saratov")

    # Задача для утреннего сообщения
    scheduler.add_job(
        send_morning_image,
        trigger="cron",
        hour=9,
        minute=0,
        kwargs={"bot": application.bot},
    )

    for day in DAYS:
        scheduler.add_job(
            send_monthly_reminder,  # Асинхронная функция
            trigger="cron",
            day=day,
            hour=9,
            minute=5,
            kwargs={
                "bot": application.bot,
                "message": f"📅 Сегодня {day}-е число! Не забудьте передать показания счетчиков!",
            },
        )

    scheduler.start()