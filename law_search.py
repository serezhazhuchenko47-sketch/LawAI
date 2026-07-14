import re


CODEX = {
    "цку": "civil",
    "кку": "criminal",
    "купап": "administrative",
    "конституція": "constitution",
}


def parse_query(query: str):
    """
    Розбирає запит типу:
    ст.1166 ЦКУ
    стаття 185 ККУ
    """

    text = query.lower()

    article = re.search(r"\d+", text)

    if not article:
        return None

    article = article.group()

    codex = None

    for key in CODEX:

        if key in text:

            codex = CODEX[key]
            break

    return {
        "article": article,
        "codex": codex,
    }