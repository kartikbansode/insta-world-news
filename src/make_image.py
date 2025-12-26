from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import os
import requests
from io import BytesIO

WIDTH = HEIGHT = 1080

def load_bg(image_url):
    if not image_url:
        return None
    try:
        r = requests.get(image_url, timeout=10)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        if img.width < 500 or img.height < 500:
            return None
        return img
    except:
        return None

def make_image(title, image_url=None):
    bg_img = load_bg(image_url)

    if bg_img:
        bg = bg_img.resize((WIDTH, HEIGHT)).filter(ImageFilter.GaussianBlur(1.5))
    else:
        bg = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 10))

    bg = bg.convert("RGBA")
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 150))
    bg = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(bg)

    try:
        font_big = ImageFont.truetype("assets/fonts/arial.ttf", 80)
        font_small = ImageFont.truetype("assets/fonts/arial.ttf", 34)
        font_tag = ImageFont.truetype("assets/fonts/arial.ttf", 30)
    except:
        font_big = font_small = font_tag = ImageFont.load_default()

    # Breaking News tag (smaller)
    tag_w, tag_h = 260, 60
    draw.rectangle((40, 40, 40 + tag_w, 40 + tag_h), fill=(210, 0, 0, 255))
    draw.text((60, 55), "BREAKING NEWS", font=font_tag, fill="white")

    # Bottom panel
    panel_top = HEIGHT - 360
    draw.rectangle((0, panel_top, WIDTH, HEIGHT), fill=(0, 0, 0, 200))

    # Headline text (bigger & higher)
    wrapped = textwrap.fill(title.upper(), width=26)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_big)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.multiline_text(
        ((WIDTH - w) / 2, panel_top + 40),
        wrapped,
        font=font_big,
        fill="white",
        align="center"
    )

    # Footer branding
    draw.text(
        (40, HEIGHT - 70),
        "Around World  @aroundworldlive",
        font=font_small,
        fill="white"
    )

    os.makedirs("output", exist_ok=True)
    path = "output/latest.png"
    bg.convert("RGB").save(path)

    return path
