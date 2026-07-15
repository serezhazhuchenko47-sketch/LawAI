from telegram import ReplyKeyboardMarkup


from telegram import ReplyKeyboardMarkup


def main_keyboard(is_admin=False):

    keyboard = [
        ["⚖️ Юридична консультація"],
        ["📄 Перевірити документ"],
        ["📝 Створити документ"],
        ["📚 Закони України"],
        ["👤 Мій профіль", "⭐ LawAI PRO"]
    ]

    if is_admin:
        keyboard.append(["🔐 Адмін-панель"])

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