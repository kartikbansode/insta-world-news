import feedparser
from newspaper import Article

FEEDS = [
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en",
    "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en",
    "https://feeds.reuters.com/reuters/worldNews",
    "http://feeds.bbci.co.uk/news/world/rss.xml"
]

def get_latest_news():
    all_entries = []

    for url in FEEDS:
        feed = feedparser.parse(url)
        all_entries.extend(feed.entries)

    all_entries = sorted(
        all_entries,
        key=lambda x: x.get("published_parsed", 0),
        reverse=True
    )

    for entry in all_entries[:10]:
        try:
            article = Article(entry.link)
            article.download()
            article.parse()

            return {
                "title": entry.title,
                "link": entry.link,
                "source": entry.get("source", {}).get("title", "News"),
                "image": article.top_image
            }
        except:
            continue

    return None
