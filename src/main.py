from fetch_news import get_latest_news
from make_image import make_image
import shutil
import os

LAST_FILE = "data/last.txt"


def main():
    news = get_latest_news()
    if not news:
        print("No news found.")
        return

    title = news["title"].strip()
    link = news["link"]

    # Read last posted title
    last_title = ""
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            last_title = f.read().strip()

    if title == last_title:
        print("Same news as last time. Skipping.")
        return

    print("New headline:", title)


path = make_image(title, news.get("image"), news.get("category", "World"))
print("Image generated at:", path)

# Make image with category
path = make_image(title, news.get("image"), news.get("category", "World"))

# Save last title
os.makedirs("data", exist_ok=True)
with open(LAST_FILE, "w", encoding="utf-8") as f:
    f.write(title)

if __name__ == "__main__":
    main()
