import re

from services.playwright_service import playwright_service
from services.document_parser import document_parser


class LawService:

   def get_article(self, law_id: str, article_number: str):

        html = playwright_service.get_html(law_id)

        if html is None:
            print("HTML = None")
            return None

        print(f"HTML length: {len(html)}")

        article_container = document_parser.get_article_container(html)

        if article_container is None:

            return None


        start = article_container.find(
            attrs={"data-tree": f"st{article_number}"}
        )

        if start is None:
            print(f"Article st{article_number} not found")
            return None

        from bs4 import Tag

        text_parts = []

        node = start.parent

        
        while node:

            if isinstance(node, Tag):

            # Якщо почалась наступна стаття — закінчуємо
                anchor = node.find("a", attrs={"data-tree": True})

            if (
                anchor
                and anchor.get("data-tree", "").startswith("st")
                and anchor.get("data-tree") != f"st{article_number}"
            ):
                break

            text = node.get_text(" ", strip=True)

            if text:
                text_parts.append(text)

            node = node.find_next_sibling()

        return "\n\n".join(text_parts)

law_service = LawService()