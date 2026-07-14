from telegram import ReplyKeyboardMarkup


def main_keyboard():
    keyboard = [
        ["⚖️ Юридична консультація"],
        ["📄 Перевірити документ"],
        ["📝 Створити документ"],
        ["📚 Закони України"],
        ["👤 Мій профіль", "⭐ LawAI PRO"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )