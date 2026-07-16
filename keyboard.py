from telegram import ReplyKeyboardMarkup


from telegram import ReplyKeyboardMarkup


def main_keyboard(is_admin=False):

    keyboard = [
        ["📂 Мої справи"],
        ["⚖️ Юридична консультація"],
        ["📄 Перевірити документ"],
        ["📝 Створити документ"],
        ["📚 Закони України"],
        ["❌ Завершити роботу з документом"],
        ["👤 Мій профіль", "⭐ LawAI PRO"],
    ]

    if is_admin:
        keyboard.append(["🔐 Адмін-панель"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

def cases_keyboard():

    keyboard = [
        ["➕ Створити справу"],
        ["⬅️ Назад"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

def admin_keyboard():

    keyboard = [
        ["👥 Користувачі", "📊 Статистика"],
        ["⭐ Видати PRO", "❌ Забрати PRO"],
        ["📢 Розсилка"],
        ["⬅️ Назад"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

from telegram import ReplyKeyboardMarkup


def admin_keyboard():

    return ReplyKeyboardMarkup(
        [
            ["👥 Користувачі", "📊 Статистика"],
            ["⭐ Видати PRO", "❌ Забрати PRO"],
            ["📢 Розсилка"],
            ["⬅️ Назад"]
        ],
        resize_keyboard=True
    )