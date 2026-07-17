import requests

url = "https://zakon.rada.gov.ua/laws/file/435-15"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("STATUS:", response.status_code)
print("CONTENT-TYPE:", response.headers.get("Content-Type"))
print("FINAL URL:", response.url)

with open("law_response.bin", "wb") as f:
    f.write(response.content)

print("Файл збережено.")