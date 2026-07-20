import re

from services.codex_registry import CODEXES


def parse_law_query(text: str):
    text_lower = text.lower()

    # Номер статті
    article_match = re.search(
    r"(?:ст\.?|стаття)\s*(\d+(?:-\d+)?)|(\d+(?:-\d+)?)",
    text_lower
    )

    if article_match is None:
        return None

    article = article_match.group(1) or article_match.group(2)

    # Кодекси
    for codex in CODEXES:
        if codex in text_lower:
            return {
                "article": article,
                "type": "codex",
                "codex": codex
            }

    # Закони
    # Закон у лапках або без лапок
    law_match = re.search(
        r'(?:закон(?:у)?(?:\s+україни)?|зу)\s*(?:[«"](.+?)[»"]|(.+))',
        text,
        re.IGNORECASE
    )

    if law_match:
        title = (law_match.group(1) or law_match.group(2)).strip()
        title = re.sub(r"\s+", " ", title)

        return {
            "article": article,
            "type": "law",
            "title": title
        }
    print(title)
    return None


def is_law_request(text: str):
    return parse_law_query(text) is not None