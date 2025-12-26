import os
from fetch_news import get_latest_news
from make_image import make_image

def main():
    news = get_latest_news()

    title = news.get("title", "Breaking News")
    image_url = news.get("image")
    category = news.get("category", "World")

    print("New headline:", title)

    path = make_image(title, image_url, category)

    print("Image generated at:", path)

if __name__ == "__main__":
    main()