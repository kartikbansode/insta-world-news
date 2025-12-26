from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import requests
from io import BytesIO

WIDTH = HEIGHT = 1080

def load_image_from_url(url):
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
        bg = load_image_from_url(image_url)

    if bg:
        bg = bg.resize((WIDTH, HEIGHT))
        img = bg
    else:
        img = Image.new("RGB", (WIDTH, HEIGHT), (30, 30, 30))

    draw = ImageDraw.Draw(img)

    # Dark gradient overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)

    for i in range(HEIGHT):
        alpha = int(180 * (i / HEIGHT))
        o_draw.line((0, i, WIDTH, i), fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_big = ImageFont.truetype("assets/fonts/arial.ttf", 64)
        font_small = ImageFont.truetype("assets/fonts/arial.ttf", 34)
        font_tag = ImageFont.truetype("assets/fonts/arial.ttf", 38)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    padding = 60

    # Category badge
    tag_text = category.upper()
    bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    draw.rectangle(
        (padding - 20, padding - 15, padding + tw + 20, padding + th + 15),
        fill=(200, 0, 0)
    )
    draw.text((padding, padding), tag_text, fill="white", font=font_tag)

    # Headline at bottom
    wrapped = textwrap.fill(title.upper(), width=28)
    hbbox = draw.multiline_textbbox((0, 0), wrapped, font=font_big)
    hw = hbbox[2] - hbbox[0]
    hh = hbbox[3] - hbbox[1]

    x = padding
    y = HEIGHT - hh - 140

    draw.multiline_text((x, y), wrapped, fill="white", font=font_big, align="left")

    # Branding
    brand = "Around World  @aroundworldlive"
    draw.text((padding, HEIGHT - 70), brand, fill="white", font=font_small)

    os.makedirs("output", exist_ok=True)
    path = "output/latest.png"
    img.save(path)

    return path
