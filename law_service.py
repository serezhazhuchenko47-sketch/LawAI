from codex_registry import CODEXES
from rada_client import rada


class LawService:

    def get_article(self, article: str, codex_key: str):

        if not codex_key:
            return None

        codex = CODEXES.get(codex_key.lower())

        if not codex:
            return None

        # Поки що підтримуємо лише ЦК України
        law_id = codex["law_id"]

        article_text = rada.get_article(
            law_id,
            article
        )

        if article_text is None:
            return None

        return {
            "codex": codex["name"],
            "article": article,
            "text": article_text
        }


law_service = LawService()