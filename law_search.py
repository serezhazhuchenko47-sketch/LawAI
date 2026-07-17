import re

from services.codex_registry import CODEXES


def parse_law_query(text: str):
    """
    Розпізнає запити типу:
    - ст. 638 ЦКУ
    - 638 ЦКУ
    - стаття 1166 Цивільного кодексу
    """

    text_lower = text.lower()

    # ---------- Пошук номера статті ----------

    article_match = re.search(
        r"(?:ст\.?|стаття)\s*(\d+)|(\d+)",
        text_lower
    )

    if article_match is None:
        return None

    article = int(article_match.group(1) or article_match.group(2))

    # ---------- Пошук кодексу ----------

    found_codex = None

    for codex in CODEXES:

        if codex in text_lower:

            found_codex = codex
            break

    if found_codex is None:
        return None

    return {
        "article": article,
        "codex": found_codex
    }


def is_law_request(text: str) -> bool:

    return parse_law_query(text) is not None