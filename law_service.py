from codex_registry import CODEXES
from rada_client import rada
from services.search_provider import search_provider


class LawService:

    def get_article(self, article: str, codex_key: str):

        codex = CODEXES.get(codex_key.lower())

        # ----------------------------
        # Якщо це відомий кодекс
        # ----------------------------

        if codex:

            law_id = codex["law_id"]

        # ----------------------------
        # Якщо це інший закон
        # ----------------------------

        else:

            result = search_provider.find_law(codex_key)

            if result is None:
                return None

            url = result["url"]

            if "/laws/show/" not in url:
                return None

            law_id = url.split("/laws/show/")[1].split("?")[0]

        article_text = rada.get_article(
            law_id,
            article
        )

        if article_text is None:
            return None

        return {
            "codex": codex_key,
            "article": article,
            "text": article_text
        }


law_service = LawService()