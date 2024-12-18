from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import TOKEN_TG


# Команда для получения Chat ID
async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID этой группы: {chat_id}")



#if __name__ == "__main__":
    # Создание приложения
    #app = ApplicationBuilder().token(TOKEN_TG).build()

    # Добавление обработчика для команды "/chatid"
    #app.add_handler(CommandHandler("chatid", chat_id))

    # Запуск бота
    #app.run_polling(x)