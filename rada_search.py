import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


BASE_URL = "https://zakon.rada.gov.ua"


def search_law(query: str):
    """
    Пошук нормативного акта на zakon.rada.gov.ua.

    Повертає:

    {
        "success": True/False,
        "url": "...",
        "title": "...",
        "message": "..."
    }
    """

    try:

        search_url = (
            f"{BASE_URL}/laws/main/index?"
            f"text={quote(query)}"
        )

        response = requests.get(
            search_url,
            timeout=20,
            headers={
                "User-Agent": "LawAI"
            }
        )

        if response.status_code != 200:

            return {
                "success": False,
                "message": "Помилка доступу до zakon.rada.gov.ua"
            }

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return {
            "success": True,
            "url": search_url,
            "title": "",
            "message": "Пошук виконано"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }