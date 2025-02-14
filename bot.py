from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers.quiz import start_quiz, handle_answer, restart_quiz

async def start(update, context):
    await update.message.reply_text("Привет! Я бот Московского зоопарка. Давай найдём тебе животное для опеки!")

if __name__ == "__main__":
    print("Бот запускается...")  # Лог для проверки
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", start_quiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
    application.add_handler(CallbackQueryHandler(restart_quiz, pattern="^restart_quiz$"))

    # Запуск бота
    print("Бот запущен и готов к работе!")  # Ещё один лог
    application.run_polling()