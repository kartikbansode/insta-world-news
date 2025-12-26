from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import requests
from io import BytesIO

WIDTH = HEIGHT = 1080

def load_image(url):
    try:
        r = requests.get(url, timeout=10)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return img
    except:
        return None

def make_image(title, image_url=None, category="World"):
    # Load background image
    bg = None
    if image_url:
        bg = load_image(image_url)

    if bg:
        bg = bg.resize((WIDTH, HEIGHT))
        img = bg
    else:
        img = Image.new("RGB", (WIDTH, HEIGHT), (20, 20, 20))

    draw = ImageDraw.Draw(img)

    # Bottom dark gradient overlay (for text readability)
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    for y in range(HEIGHT):
        if y > HEIGHT * 0.5:
            alpha = int(220 * ((y - HEIGHT * 0.5) / (HEIGHT * 0.5)))
            o_draw.line((0, y, WIDTH, y), fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Fonts (VERY BIG)
    try:
        font_head = ImageFont.truetype("assets/fonts/arial.ttf", 96)
        font_tag = ImageFont.truetype("assets/fonts/arial.ttf", 42)
        font_small = ImageFont.truetype("assets/fonts/arial.ttf", 34)
    except:
        font_head = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_small = ImageFont.load_default()

    padding = 60

    # 🔴 Top red BREAKING NEWS bar
    bar_h = 90
    draw.rectangle((0, 0, WIDTH, bar_h), fill=(210, 0, 0))
    draw.text((padding, 25), "BREAKING NEWS", font=font_tag, fill="white")

    # 📰 Headline (big, center-bottom)
    wrapped = textwrap.fill(title.upper(), width=26)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_head)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = padding
    y = HEIGHT - h - 180

    draw.multiline_text((x, y), wrapped, fill="white", font=font_head, align="left")

    # 🧾 Source text (small under headline)
    source_text = f"Source: {category}"
    draw.text((padding, y + h + 15), source_text, fill="white", font=font_small)

    # 🏷️ Footer branding
    brand = "Around World  @aroundworldlive"
    draw.text((padding, HEIGHT - 60), brand, fill="white", font=font_small)

    os.makedirs("output", exist_ok=True)
    path = "output/latest.png"
    img.save(path)

    return path
