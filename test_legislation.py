from services.legislation_service import legislation_service

result = legislation_service.get_article(
    article=638,
    codex="цку"
)

print(result["title"])
print()
print(result["text"])