
import feedparser
import random

# Tech News Feeds
FEEDS = {
    "Heise": "https://www.heise.de/rss/heise-online-atom.xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    "t3n": "https://t3n.de/rss.xml"
}

def get_latest_news(limit=3):
    """
    Fetches the latest headlines from configured feeds.
    Returns a list of dicts: {'title': ..., 'link': ..., 'source': ...}
    """
    all_news = []
    
    print("📰 Fetching Tech News...")
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                all_news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": source,
                    # Some feeds summarize in 'summary' or 'description'
                    "summary": getattr(entry, "summary", "")[:200]
                })
        except Exception as e:
            print(f"⚠️ Failed to fetch {source}: {e}")
            
    # Shuffle to not always have Heise first
    random.shuffle(all_news)
    return all_news

def pick_news_topic():
    """
    Fetches news and returns a string suitable for a 'Hint'.
    """
    news = get_latest_news(limit=2)
    if not news:
        return None
        
    # Pick one random topic
    top_story = news[0]
    return f"News Topic: {top_story['title']} (Source: {top_story['source']})"

if __name__ == "__main__":
    # Test
    print(pick_news_topic())
