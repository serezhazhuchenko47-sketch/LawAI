from dataclasses import dataclass
from bs4 import BeautifulSoup
import re


@dataclass
class LawDocument:
    title: str
    document_type: str
    number: str
    date: str
    edition: str
    text: str


class DocumentParser:

    def parse(self, html: str) -> LawDocument:

        soup = BeautifulSoup(html, "html.parser")

        title = self._get_title(soup)
        document_type = self._get_document_type(soup)
        number = self._get_number(soup)
        date = self._get_date(soup)
        edition = self._get_edition(soup)
        text = self._get_text(soup)

        return LawDocument(
            title=title,
            document_type=document_type,
            number=number,
            date=date,
            edition=edition,
            text=text
        )

    def _get_title(self, soup: BeautifulSoup) -> str:

        h1 = soup.find("h1")

        if h1:
            return self._clean(h1.get_text())

        return ""

    def _get_document_type(self, soup: BeautifulSoup) -> str:

        em = soup.find("em")

        if em:
            return self._clean(em.get_text())

        return ""

    def _get_number(self, soup: BeautifulSoup) -> str:

        text = soup.get_text(" ", strip=True)

        match = re.search(r'№\s*([A-Za-zА-Яа-яІЇЄ0-9\-\/]+)', text)

        if match:
            return match.group(1)

        return ""

    def _get_date(self, soup: BeautifulSoup) -> str:

        text = soup.get_text(" ", strip=True)

        match = re.search(r'від\s*(\d{2}\.\d{2}\.\d{4})', text)

        if match:
            return match.group(1)

        return ""

    def _get_edition(self, soup: BeautifulSoup) -> str:

        alert = soup.find("div", class_="box alert")

        if not alert:
            return ""

        text = alert.get_text(" ", strip=True)

        match = re.search(r'Редакція\s*від\s*(\d{2}\.\d{2}\.\d{4})', text)

        if match:
            return match.group(1)

        return ""

    def _get_text(self, soup: BeautifulSoup) -> str:

        article = soup.find("div", id="article")

        if article is None:
            return ""

        # Видаляємо службові елементи
        for tag in article.find_all([
            "script",
            "style",
            "link",
            "img",
            "table"
        ]):
            tag.decompose()

        text = article.get_text("\n", strip=True)

        lines = []

        for line in text.splitlines():

            line = self._clean(line)

            if not line:
                continue

            lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def _clean(text: str) -> str:

        return re.sub(r'\s+', ' ', text).strip()

    
    def get_article_container(self, html: str):
        """
        Повертає контейнер, у якому знаходиться весь текст документа.
        """

        soup = BeautifulSoup(html, "html.parser")

        return soup.find("div", id="article")
    
document_parser = DocumentParser()

