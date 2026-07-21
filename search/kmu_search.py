from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def is_kmu_request(text: str) -> bool:
    text = text.lower()
    return (
        "кму" in text
        or "пкму" in text
        or "постанова кабінету міністрів" in text
    )


def search_kmu(query: str):
    try:
        response = client.responses.create(
            model="gpt-5",
            tools=[
                {
                    "type": "web_search"
                }
            ],
            input=query
        )

        print(response.output_text)
        response = client.responses.create(
            model="gpt-5",
            tools=[{"type": "web_search"}],
            input=f"""
        Знайди офіційний документ на zakon.rada.gov.ua.

        Запит:
        {query}

        ВАЖЛИВО:
        Поверни ВИКЛЮЧНО JSON.
        Без пояснень.
        Без markdown.

        Формат:

        {{
            "title": "...",
            "url": "...",
            "document_type": "...",
            "number": "...",
            "date": "..."
        }}
        """
        )

        import json

        result = json.loads(response.output_text)
        return result

    except Exception as e:
        print(type(e).__name__)
        print(e)
        raise