import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN
from database import init_db
from handlers import start, message
from document_handlers import handle_document


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.exception("Сталася помилка:", exc_info=context.error)


# Універсальний дебаггер
async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("=" * 80)
    print(update)
    print("=" * 80)

    if update.message and update.message.document:
        print("Є DOCUMENT")


def main():

    init_db()

    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # Дебаг - ловить ВСІ повідомлення
    app.add_handler(
        MessageHandler(filters.ALL, debug),
        group=0
    )

    # Документи
    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            handle_document,
        ),
        group=1
    )

    # Текст
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message,
        ),
        group=1
    )

    app.add_error_handler(error_handler)

    print("✅ LawAI Debug Mode запущено...")

    app.run_polling()


if __name__ == "__main__":
    main()