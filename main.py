import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

print("OPENAI =", os.getenv("OPENAI_API_KEY"))
print("TOKEN =", os.getenv("TELEGRAM_TOKEN"))

# ---------------- DATABASE ----------------

conn = sqlite3.connect("lawai.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    history TEXT
)
""")

conn.commit()


def save_name(user_id, name):
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, name) VALUES (?, ?)",
        (user_id, name),
    )
    conn.commit()


def get_name(user_id):
    cursor.execute(
        "SELECT name FROM users WHERE user_id=?",
        (user_id,),
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return None


# ---------------- MEMORY ----------------

user_history = {}


# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n\n"
        "Я твій юридичний AI-помічник.\n\n"
        "Коротко опиши своє питання 😊"
    )


# ---------------- MESSAGE ----------------

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text
    user_id = update.effective_user.id

    # створюємо історію користувача
    if user_id not in user_history:
        user_history[user_id] = []

    # ---------------- ІМ'Я ----------------

    if "мене звати " in user_text.lower():

        name = user_text.lower().split("мене звати ", 1)[1].strip().title()

        save_name(user_id, name)

        user_history[user_id].append({
            "role": "user",
            "content": f"Мене звати {name}"
        })

        await update.message.reply_text(
            f"Приємно познайомитися, {name}! 😊 Я запам'ятав твоє ім'я."
        )

        return

    # ---------------- ПИТАННЯ ПРО ІМ'Я ----------------

    if "як мене звати" in user_text.lower():

        name = get_name(user_id)

        if name:
            await update.message.reply_text(
                f"Тебе звати {name}. 😊"
            )
        else:
            await update.message.reply_text(
                "Я ще не знаю твого імені.\n\nНапиши:\nМене звати ..."
            )

        return

    # ---------------- ІСТОРІЯ ----------------

    user_history[user_id].append({
        "role": "user",
        "content": user_text
    })

    # залишаємо тільки останні 20 повідомлень
    history = user_history[user_id][-20:]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
Ти досвідчений український юрист.

Ти консультуєш лише відповідно до законодавства України.

Спеціалізація:

- цивільне право;
- кримінальне право;
- адміністративне право;
- сімейне право;
- спадкове право;
- трудове право;
- земельне право.

Правила:

- відповідай українською;
- якщо бракує інформації — став уточнюючі питання;
- не вигадуй статті законів;
- пояснюй просто;
- якщо питання потребує адвоката — повідом про це.
"""
            },
            *history
        ]
    )

    answer = response.choices[0].message.content

    user_history[user_id].append({
        "role": "assistant",
        "content": answer
    })

    await update.message.reply_text(answer)


# ---------------- BOT ----------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message)
)

print("Бот запущений...")

app.run_polling()