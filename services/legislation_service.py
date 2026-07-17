from services.codex_registry import CODEXES
from services.law_service import law_service


class LegislationService:

    def get_article(self, article: int, codex: str):

        codex = codex.lower().strip()

        if codex not in CODEXES:
            return None

        law_id = CODEXES[codex]["law_id"]

        text = law_service.get_article(
            law_id=law_id,
            article_number=article
        )

        if text is None:
            return None

        return {
            "title": CODEXES[codex]["name"],
            "article": article,
            "text": text
        }


legislation_service = LegislationService()