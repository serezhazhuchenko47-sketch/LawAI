import os

from docx import Document
from docx.shared import Pt

from telegram import Update
from telegram.ext import ContextTypes

from ai import ask_ai
from prompts import GENERATOR_PROMPT
from database import save_name, get_name
from keyboard import main_keyboard
from law_search import is_law_request, parse_law_query
from law_service import law_service

# Історія діалогу
user_history = {}

# Режим роботи користувача
user_mode = {}

def create_docx(title: str, content: str) -> str:

    os.makedirs("generated", exist_ok=True)

    filename = "".join(
        c if c.isalnum() else "_"
        for c in title
    )

    filename = filename[:40]

    path = f"generated/{filename}.docx"

    doc = Document()

    heading = doc.add_heading(title, level=1)

    for run in heading.runs:
        run.font.size = Pt(18)

    doc.add_paragraph(content)

    doc.add_paragraph("\n--------------------------------")

    footer = doc.add_paragraph(
        "Створено за допомогою LawAI"
    )

    for run in footer.runs:
        run.italic = True

    doc.save(path)

    return path


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

        docx_path = create_docx(
            "Юридичний документ",
            answer
        )

        with open(docx_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename="LawAI_Document.docx",
                caption="📄 Документ готовий."
            )

        await update.message.reply_text(
            "✅ Документ успішно створено.\n\n"
            "📄 Завантажте файл DOCX вище."
        )

        os.remove(docx_path)

        user_mode[user_id] = "chat"

        return


       # ---------- Закони України ----------

    if is_law_request(text):

        law = parse_law_query(text)

        result = law_service.get_article(
            law["article"],
            law["codex"]
        )

        if result is None:

            await update.message.reply_text(
                "❌ Статтю не знайдено."
            )

            return

        explanation = ask_ai(
            [
                {
                    "role": "user",
                    "content":
                        "Поясни простими словами:\n\n"
                        + result["text"]
                }
            ]
        )

        message = (
            f"📚 {result['codex']}\n\n"
            f"{result['text']}\n\n"
            f"💡 Пояснення:\n\n"
            f"{explanation}"
        )

        MAX = 4000

        for i in range(0, len(message), MAX):

            await update.message.reply_text(
                message[i:i + MAX]
            )

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