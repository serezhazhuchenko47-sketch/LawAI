from urllib.parse import quote

from playwright.sync_api import sync_playwright


class DocumentSearch:

    @staticmethod
    def search_law_by_title(title: str):

        url = (
            "https://zakon.rada.gov.ua/laws/find/a?text="
            + quote(title)
        )

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(url)

            page.wait_for_load_state("networkidle")

            current_url = page.url

            browser.close()

        if "/laws/main/" not in current_url:
            return None

        law_id = (
            current_url
            .split("/laws/main/")[1]
            .split("#")[0]
        )

        # Якщо сайт повернув кілька документів:
        # 1402-19,2453-17 -> 1402-19
        if "," in law_id:
            law_id = law_id.split(",")[-1]

        return law_id