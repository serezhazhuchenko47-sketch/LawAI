from services.codex_registry import CODEXES
from services.law_service import law_service


class LegislationService:

    def get_article(self, article: int, document: str):

        document = document.strip()

        # Якщо це кодекс
        key = document.lower()
        if key in CODEXES:
            law_id = CODEXES[key]["law_id"]
            title = CODEXES[key]["name"]
        else:
            # Інакше вважаємо, що це вже law_id
            law_id = document
            title = None

        text = law_service.get_article(
            law_id=law_id,
            article_number=article
        )

        if text is None:
            return None

        return {
            "title": title or f"Закон № {law_id}",
            "article": article,
            "text": text
        }


legislation_service = LegislationService()