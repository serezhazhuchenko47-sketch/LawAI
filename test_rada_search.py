import requests

URL = (
    "https://zakon.rada.gov.ua/laws/main/index"
)

params = {
    "text": "Цивільний кодекс України"
}

print("Відправляю запит...")

response = requests.get(
    URL,
    params=params,
    headers={
        "User-Agent": "LawAI"
    },
    allow_redirects=True,
    timeout=30
)

print()
print("HTTP:", response.status_code)
print("URL після редиректів:")
print(response.url)

print()
print("===== Перші 5000 символів =====")
print(response.text[:5000])

print()
print("===== Кінець =====")