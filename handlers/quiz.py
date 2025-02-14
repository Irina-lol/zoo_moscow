# handlers/quiz.py
import json
from telegram import Update
from telegram.ext import CallbackContext


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