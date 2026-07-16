import re

from codex_registry import CODEXES


def parse_law_query(text: str):
    """
    Шукає номер статті та кодекс у повідомленні.
    Приклад:
    ст. 1166 ЦКУ
    стаття 625 Цивільного кодексу
    """

    text_lower = text.lower()

    article_match = re.search(
    r"(?:ст\.?|стаття)\s*(\d+)|(\d+)\s*статт[іяєї]*",
    text_lower
    )

    if not article_match:
        return None

    article = article_match.group(1) or article_match.group(2)

    found_codex = None

    for key in CODEXES.keys():

        if key.lower() in text_lower:
            found_codex = key
            break

    if not found_codex:
        return None

    return {
        "article": article,
        "codex": found_codex
    }


def is_law_request(text: str) -> bool:
    """
    Перевіряє, чи повідомлення схоже на запит статті закону.
    """

    return parse_law_query(text) is not None