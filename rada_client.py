import re
import requests


class RadaClient:

    BASE_URL = "https://data.rada.gov.ua/laws/show"

    def __init__(self, timeout=30):
        self.timeout = timeout

    def download_law(self, law_id: str):
        """
        Завантажує офіційний текст закону.
        Якщо сайт Ради недоступний — повертає None.
        """

        url = f"{self.BASE_URL}/{law_id}.txt"

        try:

            response = requests.get(
                url,
                headers={
                    "User-Agent": "LawAI"
                },
                timeout=self.timeout
            )

            response.raise_for_status()

            return response.text

        except requests.RequestException as e:

            print(f"RADA ERROR: {e}")

            return None

    def get_article(self, law_id: str, article: str):
        """
        Повертає текст статті за ID нормативного акта.
        """

        text = self.download_law(law_id)

        if text is None:
            return None

        pattern = (
            rf"Стаття\s+{re.escape(article)}\.(.*?)(?=\nСтаття\s+\d+[¹²³⁴⁵⁶⁷⁸⁹⁰-]*\.|\Z)"
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