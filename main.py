import logging

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
from photo_handlers import handle_photo


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def error_handler(update, context: ContextTypes.DEFAULT_TYPE):
    logging.exception(
        "Сталася помилка:",
        exc_info=context.error
    )


def main():

    # Ініціалізація бази
    init_db()

    # Створення Telegram Application
    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    # Команда /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # PDF / DOCX
    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            handle_document
        )
    )

    # Фото документів
    app.add_handler(
    MessageHandler(
        filters.PHOTO,
        handle_photo
    )
)

    # Текстові повідомлення
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message
        )
    )

    # Логування помилок
    app.add_error_handler(error_handler)

    print("=" * 50)
    print("⚖️ LawAI v1.0")
    print("Бот успішно запущений.")
    print("=" * 50)

    app.run_polling()


if __name__ == "__main__":
    main()