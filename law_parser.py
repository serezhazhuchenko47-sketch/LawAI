from bs4 import BeautifulSoup


class LawParser:

    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    def find_article(self, article_number: str):
        """
        Пошук статті у документі.

        Поки що повертає весь текст документа.
        На наступному кроці зробимо точний пошук статті.
        """

        text = self.soup.get_text(
            separator="\n",
            strip=True
        )

        return {
            "success": True,
            "article": article_number,
            "text": text
        }