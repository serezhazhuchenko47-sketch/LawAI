from services.law_service import law_service

article = law_service.get_article(
    "435-15",
    638
)

print(article)