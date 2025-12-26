from fetch_news import get_latest_news
from make_image import make_image

def main():
    news = get_latest_news()
    if not news:
        print("No news found.")
        return

    print("Headline:", news["title"])
    make_image(news["title"], news.get("image"))

if __name__ == "__main__":
    main()
