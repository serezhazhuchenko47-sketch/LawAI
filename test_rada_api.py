import requests

URL = "https://data.rada.gov.ua/laws/show/435-15.txt"

headers = {
    "User-Agent": "OpenData"
}

print("Запит...")

response = requests.get(
    URL,
    headers=headers,
    timeout=30
)

print("HTTP:", response.status_code)

print("\nПерші 3000 символів:\n")

print(response.text[:3000])