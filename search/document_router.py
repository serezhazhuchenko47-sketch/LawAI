import re

def detect_document_type(text: str) -> str:
    text = text.lower()

    if "постанова кму" in text or "кабінет міністрів" in text:
        return "KMU"

    if "наказ" in text:
        return "ORDER"

    if "єспл" in text or "v. ukraine" in text:
        return "ECHR"

    if "справа №" in text.lower() or "верховний суд" in text.lower():
        return "COURT"

    return "LAW"