from services.playwright_service import playwright_service

html = playwright_service.get_html("435-15")

if html:

    print("OK")
    print(len(html))

    with open("rada.html", "w", encoding="utf-8") as f:
        f.write(html)

else:

    print("ERROR")