import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise ValueError(
        "Не знайдено TELEGRAM_TOKEN у файлі .env"
    )

if not OPENAI_API_KEY:
    raise ValueError(
        "Не знайдено OPENAI_API_KEY у файлі .env"
    )