import re


def is_law_request(text: str) -> bool:
    """
    Перевіряє, чи користувач запитує статтю закону.
    """

    text = text.lower()

    keywords = [
        "ст.",
        "стаття",
        "цку",
        "кку",
        "купап",
        "конституція",
        "закон"
    ]

    return any(word in text for word in keywords)


def get_law_answer(text: str) -> str:
    """
    Тимчасова відповідь.
    На наступному етапі буде використовуватись база законів.
    """

    article = re.search(r"\d+", text)

    if article:

        return (
            f"🔎 Запит щодо статті {article.group()} отримано.\n\n"
            "У наступній версії LawAI буде автоматичний пошук "
            "актуальної редакції закону."
        )

    return (
        "🔎 Пошук законодавства буде доступний "
        "у наступному оновленні LawAI."
    )