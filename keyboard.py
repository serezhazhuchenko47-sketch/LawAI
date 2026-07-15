from telegram import ReplyKeyboardMarkup


def main_keyboard():

    keyboard = [
        ["⚖️ Юридична консультація"],
        ["📄 Перевірити документ"],
        ["📝 Створити документ"],
        ["📚 Закони України"],
        ["👤 Мій профіль", "⭐ LawAI PRO"],
        ["🔐 Адмін-панель"]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )