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
    # Try to load background image
    bg = None
    if image_url:
        bg = load_image(image_url)

    if bg:
        bg = bg.resize((WIDTH, HEIGHT))
        img = bg
    else:
        img = Image.new("RGB", (WIDTH, HEIGHT), (25, 25, 25))

    # Add dark overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 160))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)

    # Fonts (BIG)
    try:
        font_head = ImageFont.truetype("assets/fonts/arial.ttf", 90)
        font_tag = ImageFont.truetype("assets/fonts/arial.ttf", 48)
        font_brand = ImageFont.truetype("assets/fonts/arial.ttf", 40)
    except:
        font_head = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_brand = ImageFont.load_default()

    padding = 60

    # Category badge (top-left)
    tag = category.upper()
    tb = draw.textbbox((0, 0), tag, font=font_tag)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]

    draw.rectangle(
        (padding - 20, padding - 15, padding + tw + 20, padding + th + 15),
        fill=(220, 0, 0)
    )
    draw.text((padding, padding), tag, fill="white", font=font_tag)

    # Headline (BOTTOM, VERY BIG)
    wrapped = textwrap.fill(title.upper(), width=24)
    hb = draw.multiline_textbbox((0, 0), wrapped, font=font_head)
    hw = hb[2] - hb[0]
    hh = hb[3] - hb[1]

    x = padding
    y = HEIGHT - hh - 150

    draw.multiline_text((x, y), wrapped, fill="white", font=font_head, align="left")

    # Branding bottom-left
    brand = "Around World  @aroundworldlive"
    draw.text((padding, HEIGHT - 60), brand, fill="white", font=font_brand)

    os.makedirs("output", exist_ok=True)
    path = "output/latest.png"
    img.save(path)

    return path
