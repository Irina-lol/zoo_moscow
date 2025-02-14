import json
import logging
from telegram import Update
from telegram.ext import CallbackContext
from utils.images import get_animal_image
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def start_quiz(update: Update, context: CallbackContext):
    with open("data/questions.json", "r", encoding="utf-8") as file:
        questions = json.load(file)

    context.user_data["quiz"] = {
        "current_question": 0,
        "answers": {},
        "questions": questions
    }

    await ask_question(update, context)


async def ask_question(update: Update, context: CallbackContext):
    quiz_data = context.user_data["quiz"]
    current_question = quiz_data["current_question"]
    questions = quiz_data["questions"]

    if current_question >= len(questions):
        await finish_quiz(update, context)
        return

    question = questions[current_question]
    options = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(question["options"])])

    await update.message.reply_text(f"{question['question']}\n{options}")


async def handle_answer(update: Update, context: CallbackContext):
    answer = update.message.text
    quiz_data = context.user_data["quiz"]
    current_question = quiz_data["current_question"]
    questions = quiz_data["questions"]

    quiz_data["answers"][current_question] = answer
    quiz_data["current_question"] += 1

    await ask_question(update, context)


async def finish_quiz(update: Update, context: CallbackContext):
    quiz_data = context.user_data["quiz"]
    answers = quiz_data["answers"]
    questions = quiz_data["questions"]

    scores = {"сурикат": 0, "фламинго": 0, "лев": 0}

    for i, answer in answers.items():
        question = questions[i]
        weights = question["weights"][answer]
        for animal, weight in weights.items():
            scores[animal] += weight

    result = max(scores, key=scores.get)
    await update.message.reply_text(f"Твоё животное — {result}!")

    try:
        # Отправка изображения
        image = get_animal_image(result)
        await update.message.reply_photo(photo=image)
    except FileNotFoundError as e:
        logging.error(f"Ошибка при отправке изображения: {e}")
        await update.message.reply_text("Извините, изображение не найдено.")
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {e}")
        await update.message.reply_text("Что-то пошло не так. Попробуйте позже.")

    # Кнопка для публикации результата
    keyboard = [
        [InlineKeyboardButton("Поделиться результатом", url=f"https://t.me/share/url?url=Моё животное — {result}!")],
        [InlineKeyboardButton("Попробовать ещё раз", callback_data="restart_quiz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Поделись результатом с друзьями или попробуй ещё раз!", reply_markup=reply_markup)

