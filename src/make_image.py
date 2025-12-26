from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import requests
from io import BytesIO

WIDTH = HEIGHT = 1080

def load_bg(image_url):
    try:
        r = requests.get(image_url, timeout=10)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return img.resize((WIDTH, HEIGHT))
    except:
        return Image.new("RGB", (WIDTH, HEIGHT), (20, 20, 20))

def make_image(title, image_url=None):
    bg = load_bg(image_url)
    draw = ImageDraw.Draw(bg)

    # Dark overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 160))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(bg)

    try:
        font_big = ImageFont.truetype("assets/fonts/arial.ttf", 64)
        font_small = ImageFont.truetype("assets/fonts/arial.ttf", 36)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Top red bar
    draw.rectangle((0, 0, WIDTH, 120), fill=(200, 0, 0, 255))
    draw.text((40, 30), "BREAKING NEWS", font=font_small, fill="white")

    wrapped = textwrap.fill(title.upper(), width=22)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_big)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.multiline_text(
        ((WIDTH - w) / 2, (HEIGHT - h) / 2),
        wrapped,
        font=font_big,
        fill="white",
        align="center"
    )

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
