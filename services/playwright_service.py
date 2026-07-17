from playwright.sync_api import sync_playwright


class PlaywrightService:
    """
    Завантажує повністю відрендерену сторінку
    zakon.rada.gov.ua разом із текстом документа.
    """

    def __init__(self, timeout: int = 30000):
        self.timeout = timeout

    def get_html(self, law_id: str) -> str | None:

        url = f"https://zakon.rada.gov.ua/laws/show/{law_id}"

        try:

            with sync_playwright() as p:

                browser = p.chromium.launch(
                    headless=True
                )

                page = browser.new_page()

                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=self.timeout
                )

                # Даємо JavaScript завершити рендеринг
                page.wait_for_timeout(2000)

                html = page.content()
                print(f"HTML length: {len(html)}")
                browser.close()

                return html

        except Exception as e:

            print(f"PLAYWRIGHT ERROR: {e}")

            return None


playwright_service = PlaywrightService()