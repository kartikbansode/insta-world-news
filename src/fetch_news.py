import feedparser
from newspaper import Article

RSS_FEEDS = [
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.espncricinfo.com/rss/content/story/feeds/0.xml",
    "https://feeds.feedburner.com/ndtvnews-top-stories"
]

def get_latest_news():
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            try:
                article = Article(entry.link)
                article.download()
                article.parse()

                # Simple category detection
                category = "World"
                src = entry.get("source", {}).get("title", "").lower()

                if "sport" in src or "cric" in src or "espn" in url:
                    category = "Sports"
                elif "tech" in src:
                    category = "Tech"
                elif "business" in src:
                    category = "Business"

                return {
                    "title": entry.title,
                    "link": entry.link,
                    "source": entry.get("source", {}).get("title", "News"),
                    "image": article.top_image,
                    "category": category
                }

            except Exception as e:
                print("Error parsing article:", e)
                continue

    return None
