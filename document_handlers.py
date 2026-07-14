import os

from telegram import Update
from telegram.ext import ContextTypes

from ai import ask_ai
from documents import extract_text
from prompts import DOCUMENT_PROMPT


async def handle_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        document = update.message.document

        if document is None:
            return

        await update.message.reply_text(
            "📄 Документ отримано.\n\nПочинаю аналіз..."
        )

        os.makedirs("temp", exist_ok=True)

        file = await context.bot.get_file(
            document.file_id
        )

        file_path = os.path.join(
            "temp",
            document.file_name
        )

        await file.download_to_drive(file_path)

        text = extract_text(file_path)

        if not text:

            await update.message.reply_text(
                "❌ Не вдалося прочитати текст документа."
            )

            return

        history = [
            {
                "role": "user",
                "content":
                    "Проаналізуй цей документ:\n\n" + text
            }
        ]

        answer = ask_ai(
            history,
            DOCUMENT_PROMPT
        )

        await update.message.reply_text(answer)

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:

        print("DOCUMENT ERROR:", e)

        await update.message.reply_text(
            f"❌ Помилка:\n{e}"
        )