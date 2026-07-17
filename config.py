import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = "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"

if not TOKEN:
    raise ValueError(
        "Не знайдено TELEGRAM_TOKEN у файлі .env"
    )

if not OPENAI_API_KEY:
    raise ValueError(
        "Не знайдено OPENAI_API_KEY у файлі .env"
    )