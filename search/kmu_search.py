from openai import OpenAI
from config import OPENAI_API_KEY
from cache import get_cache, save_cache
import json

client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=500,
    max_retries=0
)


def is_kmu_request(text: str) -> bool:
    text = text.lower()
    return (
        "кму" in text
        or "пкму" in text
        or "постанова кабінету міністрів" in text
        or "постанова кабміну" in text
        or "постанова кму" in text
    )


def search_kmu(query: str):
    # Перевіряємо кеш
    cached = get_cache(query)

    if cached:
        print("✅ CACHE")
        return cached

    try:
        response = client.responses.create(
            model="gpt-5",
            tools=[
                {
                    "type": "web_search"
                }
            ],
            instructions="""
Ти юридичний пошуковий модуль LawAI.

Правила:

1. Шукай офіційний документ на zakon.rada.gov.ua.
2. Якщо користувач вказав лише номер постанови КМУ — спочатку знайди найбільш актуальну чинну постанову.
3. Якщо існує кілька постанов з однаковим номером — поверни короткий список (номер, дата, назва), а не став загальні уточнюючі питання.
4. Повертай тільки JSON.
5. Не використовуй markdown.
6. Не додавай пояснень.

Формат відповіді:

{
    "title": "...",
    "url": "...",
    "document_type": "...",
    "number": "...",
    "date": "..."
}
""",
            input=f"""
Запит:
{query}
"""
        )

        print(response.output_text)

        result = json.loads(response.output_text)

        save_cache(query, result)

        return result
    
        # result = json.loads(response.output_text)
        # save_cache(query, result)
        # return result

    
    except json.JSONDecodeError as e:
        print("JSON ERROR")
        print(response.output_text)
        print(e)

        return {
            "title": "⚠️ OpenAI повернув некоректний JSON.",
            "url": "",
            "document_type": "",
            "number": "",
            "date": ""
        }

    except Exception as e:

        print(type(e).__name__)
        print(e)

        return {
            "title": "⚠️ Сервіс пошуку тимчасово недоступний (rada.gov.ua). Спробуйте ще раз через хвилину.",
            "url": "",
            "document_type": "",
            "number": "",
            "date": ""
        }