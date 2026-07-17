import re

from services.playwright_service import playwright_service
from services.document_parser import document_parser


class LawService:

    def get_article(self, law_id: str, article_number: int):

        html = playwright_service.get_html(law_id)

        if html is None:
            print("HTML = None")
            return None

        print(f"HTML length: {len(html)}")

        article_container = document_parser.get_article_container(html)

        if article_container is None:
            print("article_container = None")
            return None

        print("article_container found")

        start = article_container.find(
            attrs={"data-tree": f"st{article_number}"}
        )

        if start is None:
            print(f"Article st{article_number} not found")
            return None

        print(f"Article st{article_number} found")


law_service = LawService()