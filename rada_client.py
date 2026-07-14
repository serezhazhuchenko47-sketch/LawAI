import re
import requests


class RadaClient:

    BASE_URL = "https://data.rada.gov.ua/laws/show"

    def __init__(self, timeout=30):
        self.timeout = timeout

    def download_law(self, law_id: str) -> str:
        """
        Завантажує офіційний текст закону у форматі TXT.
        Приклад:
        435-15 -> ЦК України
        """

        url = f"{self.BASE_URL}/{law_id}.txt"

        response = requests.get(
            url,
            headers={
                "User-Agent": "OpenData"
            },
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.text

    def get_article(self, law_id: str, article: str):
        """
        Повертає текст статті.
        """

        text = self.download_law(law_id)

        pattern = (
            rf"Стаття\s+{article}\.(.*?)(?=\nСтаття\s+\d+\.|\Z)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.DOTALL
        )

        if not match:
            return None

        return match.group(0).strip()


rada = RadaClient()