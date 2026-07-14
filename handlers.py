from telegram import Update
from telegram.ext import ContextTypes

from ai import ask_ai
from prompts import GENERATOR_PROMPT
from database import save_name, get_name
from keyboard import main_keyboard

# Історія діалогу
user_history = {}

# Режим роботи користувача
user_mode = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Вітаю!\n\n"
        "Я LawAI — юридичний AI-помічник.\n\n"
        "Оберіть потрібний розділ нижче 👇",
        reply_markup=main_keyboard()
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_history:
        user_history[user_id] = []

    # ---------- Кнопки ----------

    if text == "⚖️ Юридична консультація":

        user_mode[user_id] = "chat"

        await update.message.reply_text(
            "Опишіть вашу юридичну ситуацію."
        )

        return

    if text == "📄 Перевірити документ":

        user_mode[user_id] = "document"

        await update.message.reply_text(
            "Надішліть PDF або DOCX документ."
        )

        return

    if text == "📝 Створити документ":

        user_mode[user_id] = "generator"

        await update.message.reply_text(
            "Який документ потрібно створити?"
        )

        return

    if text == "📚 Закони України":

        await update.message.reply_text(
            "Пошук законів буде додано на наступному етапі."
        )

        return

    if text == "👤 Мій профіль":

        name = get_name(user_id)

        if not name:
            name = "Невідомо"

        await update.message.reply_text(
            f"👤 Ваш профіль\n\n"
            f"Ім'я: {name}"
        )

        return

    if text == "⭐ LawAI PRO":

        await update.message.reply_text(
            "🚀 LawAI PRO скоро стане доступним."
        )

        return

    # ---------- Запам'ятати ім'я ----------

    if text.lower().startswith("мене звати"):

        name = text[11:].strip().title()

        if name:

            save_name(user_id, name)

            await update.message.reply_text(
                f"Приємно познайомитися, {name}! 😊"
            )

        return

    # ---------- Моє ім'я ----------

    if "як мене звати" in text.lower():

        name = get_name(user_id)

        if name:

            await update.message.reply_text(
                f"Тебе звати {name} 😊"
            )

        else:

            await update.message.reply_text(
                "Я ще не знаю твого імені."
            )

        return

    # ---------- Генерація документів ----------

    if user_mode.get(user_id) == "generator":

        answer = ask_ai(
            [
                {
                    "role": "user",
                    "content": text
                }
            ],
            system_prompt=GENERATOR_PROMPT
        )

        await update.message.reply_text(answer)

        user_mode[user_id] = "chat"

        return

    # ---------- AI ----------

    user_history[user_id].append(
        {
            "role": "user",
            "content": text
        }
    )

    answer = ask_ai(
        user_history[user_id][-20:]
    )

    user_history[user_id].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    await update.message.reply_text(answer)