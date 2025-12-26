from fetch_news import get_latest_news
from make_image import make_image
import shutil

def main():
    news = get_latest_news()
    if not news:
        print("No news found.")
        return

    print("Headline:", news["title"])
    path = make_image(news["title"], news.get("image"))

    # Copy to repo root for GitHub Pages
    shutil.copy(path, "latest.png")

if __name__ == "__main__":
    main()
