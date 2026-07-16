import os

from telegram import Update
from telegram.ext import ContextTypes

import handlers

from ai import ask_ai_image


async def handle_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        photos = update.message.photo

        if not photos:
            return

        await update.message.reply_text(
            "📷 Фотографію отримано.\n\n"
            "🔍 Аналізую документ..."
        )

        os.makedirs("temp", exist_ok=True)

        photo = photos[-1]

        telegram_file = await context.bot.get_file(
            photo.file_id
        )

        file_path = os.path.join(
            "temp",
            f"{photo.file_id}.jpg"
        )

        await telegram_file.download_to_drive(file_path)

        text = ask_ai_image(
            file_path,
            (
            "Ти професійна OCR-система для юридичних документів.\n\n"
            "Твоє завдання:\n"
            "1. Максимально точно розпізнати ВЕСЬ текст.\n"
            "2. Не аналізуй документ.\n"
            "3. Не скорочуй текст.\n"
            "4. Не переписуй своїми словами.\n"
            "5. Збережи структуру документа.\n"
            "6. Якщо слово нерозбірливе — напиши [нерозбірливо].\n"
            "7. Не додавай власних коментарів.\n\n"
            "Поверни тільки текст документа."
            )
        )

        handlers.document_context[
            update.effective_user.id
        ] = text

        await update.message.reply_text(
            "✅ Документ успішно зчитано.\n\n"
            "Тепер можете:\n"
            "• поставити питання по документу;\n"
            "• попросити написати відзив;\n"
            "• скласти клопотання;\n"
            "• створити інший юридичний документ."
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:

        print("PHOTO ERROR:", e)

        try:

            if "file_path" in locals() and os.path.exists(file_path):
                os.remove(file_path)

        except Exception:
            pass

        try:

            await update.message.reply_text(
                f"❌ Помилка під час обробки фотографії:\n\n{e}"
            )

        except Exception:
            pass