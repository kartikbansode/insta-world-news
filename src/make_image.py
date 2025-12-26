import os
from playwright.sync_api import sync_playwright

def make_image(title, image_url, category="World"):
    with open("src/template.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("{{HEADLINE}}", title.upper())
    html = html.replace("{{IMAGE_URL}}", image_url or "")

    os.makedirs("output", exist_ok=True)
    html_path = "output/card.html"
    out_path = "output/latest.png"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.screenshot(path=out_path)
        browser.close()

    return out_path
