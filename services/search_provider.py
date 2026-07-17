import requests

from config import TAVILY_API_KEY


class SearchProvider:

    URL = "https://api.tavily.com/search"

    def find_law(self, query: str):

        payload = {
            "api_key": TAVILY_API_KEY,
            "query": f"site:zakon.rada.gov.ua {query}",
            "search_depth": "basic",
            "max_results": 1
        }

        response = requests.post(
            self.URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        return results[0]


search_provider = SearchProvider()