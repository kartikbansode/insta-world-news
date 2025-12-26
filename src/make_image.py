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
        return img
    except:
        return None

def make_image(title, image_url=None):
    bg_img = load_bg(image_url)

    if bg_img:
        bg = bg_img.resize((WIDTH, HEIGHT)).filter(ImageFilter.GaussianBlur(2))
    else:
        bg = Image.new("RGB", (WIDTH, HEIGHT), (15, 15, 15))

    bg = bg.convert("RGBA")

    # Dark overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 160))
    bg = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(bg)

    # Fonts
    try:
        font_big = ImageFont.truetype("assets/fonts/arial.ttf", 70)
        font_small = ImageFont.truetype("assets/fonts/arial.ttf", 36)
        font_tag = ImageFont.truetype("assets/fonts/arial.ttf", 34)
    except:
        font_big = font_small = font_tag = ImageFont.load_default()

    # Top tag
    tag_w, tag_h = 320, 70
    draw.rectangle((40, 40, 40 + tag_w, 40 + tag_h), fill=(200, 0, 0, 255))
    draw.text((60, 55), "BREAKING NEWS", font=font_tag, fill="white")

    # Bottom panel
    panel_top = HEIGHT - 420
    draw.rectangle((0, panel_top, WIDTH, HEIGHT), fill=(0, 0, 0, 180))

    # Headline
    wrapped = textwrap.fill(title.upper(), width=28)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_big)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.multiline_text(
        ((WIDTH - w) / 2, panel_top + 60),
        wrapped,
        font=font_big,
        fill="white",
        align="center"
    )

    # Footer branding
    draw.text(
        (40, HEIGHT - 80),
        "Around World  @aroundworldlive",
        font=font_small,
        fill="white"
    )

    os.makedirs("output", exist_ok=True)
    path = "output/latest.png"
    bg.convert("RGB").save(path)

    return path
