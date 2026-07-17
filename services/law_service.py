import re

from services.playwright_service import playwright_service
from services.document_parser import document_parser


class LawService:

    def get_article(self, law_id: str, article_number: int):

        html = playwright_service.get_html(law_id)

        if html is None:
            return None

        article_container = document_parser.get_article_container(html)

        if article_container is None:
            return None

        start = article_container.find(
            attrs={"data-tree": f"st{article_number}"}
        )

        if start is None:
            return None

        result = []

        current = start.parent

        while current:

            # Якщо знайшли наступну статтю — завершуємо
            anchor = current.find(attrs={"data-tree": True})

            if (
                anchor
                and anchor != start
                and anchor["data-tree"].startswith("st")
            ):
                break

            text = current.get_text(" ", strip=True)

            if text:
                result.append(text)

            current = current.find_next_sibling()

        return "\n".join(result)


law_service = LawService()