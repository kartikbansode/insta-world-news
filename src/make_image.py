import os
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

TEMPLATE_PATH = "src/template.html"
OUTPUT_PATH = "latest.png"
FONT_PATH = "assets/Arial-Bold.ttf"

WIDTH = 2160
HEIGHT = 2160

def auto_font_size(text, max_width, max_size=152, min_size=84):
    img = Image.new("RGB", (3000, 3000))
    draw = ImageDraw.Draw(img)

    for size in range(max_size, min_size - 1, -4):
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.multiline_textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            return size
    return min_size

def make_image(headline, image_url, category="World"):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    headline = headline.upper()

    max_text_width = WIDTH - 160*2 - 20 - 50
    font_size = auto_font_size(headline, max_text_width)

    html = template \
        .replace("{{HEADLINE}}", headline) \
        .replace("{{IMAGE_URL}}", image_url or "") \
        .replace("{{FONT_SIZE}}", str(font_size))

    with open("render.html", "w", encoding="utf-8") as f:
        f.write(html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        page.goto(f"file://{os.path.abspath('render.html')}")
        page.screenshot(path="temp.png")
        browser.close()

    img = Image.open("temp.png")
    img = img.resize((1080, 1080), Image.LANCZOS)
    img.save(OUTPUT_PATH, quality=95)

    os.remove("temp.png")
    os.remove("render.html")

    return OUTPUT_PATH