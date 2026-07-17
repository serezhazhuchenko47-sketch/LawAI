from services.playwright_service import playwright_service
from services.document_parser import document_parser

html = playwright_service.get_html("435-15")

article = document_parser.get_article_container(html)

print(article is not None)

print(article["id"])