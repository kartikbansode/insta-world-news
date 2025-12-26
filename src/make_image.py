from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

WIDTH = HEIGHT = 1080

def make_image(title):
    # Create dark background
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    # Load fonts (fallback if not found)
    try:
        font_big = ImageFont.truetype("assets/fonts/arial.ttf", 64)
        font_small = ImageFont.truetype("assets/fonts/arial.ttf", 36)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Top red bar
    draw.rectangle((0, 0, WIDTH, 120), fill=(200, 0, 0))
    draw.text((40, 30), "BREAKING NEWS", font=font_small, fill="white")

    # Wrap headline
    wrapped = textwrap.fill(title.upper(), width=22)

    # Calculate text size (new Pillow method)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_big)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Draw headline centered
    draw.multiline_text(
        ((WIDTH - w) / 2, (HEIGHT - h) / 2),
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

    # Save output
    os.makedirs("output", exist_ok=True)
    path = "output/latest.png"
    img.save(path)

    return path
