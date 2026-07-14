import io
import zipfile
import requests

URL = "https://data.rada.gov.ua/ogd/zak/perv/texts-xml.zip"

print("=== Починаємо ===")

response = requests.get(URL, timeout=60)

print("HTTP:", response.status_code)

response.raise_for_status()

archive = zipfile.ZipFile(io.BytesIO(response.content))

files = archive.namelist()

print(f"Знайдено файлів: {len(files)}")

print("\nПерші 20 файлів:\n")

for name in files[:20]:
    print(name)

first = files[0]

print("\nВідкриваємо:", first)

xml = archive.read(first)

print("\nПерші 2000 байтів:\n")

print(xml[:2000])