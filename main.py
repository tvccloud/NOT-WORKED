import os
import random
import time
from pytrends.request import TrendReq
import tweepy
from transformers import pipeline

# Twitter auth
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

# AI classifier
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    token=os.getenv("HF_TOKEN")
)

# Blacklist
BLOCKED = [
    "politics","election","government","minister",
    "religion","god","hindu","islam","christian","temple","mosque"
]

def is_safe(topic):
    if any(word in topic.lower() for word in BLOCKED):
        return False
    result = classifier(topic, ["Politics","Religion","Technology","Business","Entertainment","Lifestyle"])
    for label, score in zip(result["labels"], result["scores"]):
        if label in ["Politics","Religion"] and score > 0.2:
            return False
    return True

def get_trends():
    pytrends = TrendReq()
    trends = pytrends.trending_searches(pn="india")
    return trends[0].tolist()

def generate_tweet(topic):
    return f"{topic} is gaining traction today. Worth keeping an eye on."

def main():
    topics = get_trends()
    safe_topics = [t for t in topics if is_safe(t)]
    selected = safe_topics[:5]

    for topic in selected:
        tweet = generate_tweet(topic)
        client.create_tweet(text=tweet)
        time.sleep(random.randint(3600, 7200))

if __name__ == "__main__":
    main()
