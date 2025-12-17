import os
import random
import time
import tweepy
import feedparser

# Twitter auth
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

# Strict blacklist
BLOCKED = [
    "politics", "election", "government", "minister",
    "bjp", "congress", "parliament", "president",
    "religion", "god", "hindu", "islam", "christian",
    "temple", "mosque", "church"
]

def is_safe(text):
    text = text.lower()
    return not any(word in text for word in BLOCKED)

def get_trending_topics():
    feed = feedparser.parse(
        "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    )

    topics = []
    for entry in feed.entries:
        title = entry.title
        if is_safe(title):
            topics.append(title)

    return topics[:5]

def generate_tweet(topic):
    templates = [
        f"{topic}. This is picking up momentum.",
        f"A lot of people are talking about this: {topic}",
        f"This topic is trending right now: {topic}",
        f"Seeing increased buzz around {topic}.",
        f"{topic} is gaining attention today."
    ]
    return random.choice(templates)

def main():
    topics = get_trending_topics()

    if not topics:
        return

    for topic in topics:
        tweet = generate_tweet(topic)
        client.create_tweet(text=tweet)
        time.sleep(random.randint(3600, 7200))

if __name__ == "__main__":
    main()
