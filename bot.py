# bot.py
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from telegram.ext import CommandHandler, MessageHandler, filters
from handlers.quiz import start_quiz, handle_answer

async def start(update, context):
    await update.message.reply_text("Привет! Я бот Московского зоопарка. Давай найдём тебе животное для опеки!")

if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", start_quiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    # Запуск бота
    application.run_polling()