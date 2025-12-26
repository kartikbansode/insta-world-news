from fetch_news import get_latest_news
from make_image import make_image
from post_instagram import post_to_instagram
import shutil

def main():
    news = get_latest_news()
    if not news:
        print("No news found.")
        return

    title = news["title"]
    link = news["link"]

    print("Headline:", title)

    path = make_image(title, news.get("image"))

    # Copy to repo root for GitHub Pages (still useful)
    shutil.copy(path, "latest.png")

    caption = f"""{title}

Source: {link}

#breakingnews #worldnews #globalnews #usa #uk #india #australia
#aroundworld #newsupdate
"""

    post_to_instagram(path, caption)

if __name__ == "__main__":
    main()
