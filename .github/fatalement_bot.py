from datetime import datetime, timedelta
import os

import feedparser
import pytz
import tweepy

#Twitter keys
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


def _tweet_article(api, article):
    text = f"I wrote a new article called '{article.title}'! \nYou can read it {article.link}"
    print(f'will tweet about {article.title}')
    api.update_status(text)


def get_articles():
    previous_hour = datetime.today().replace(tzinfo=pytz.utc) - timedelta(hours=10)
    feed_url = "https://fatalement.com/feed.xml"
    blog_feed = feedparser.parse(feed_url)

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    for article in blog_feed.entries:
        article_date = datetime.strptime(article.published, '%a, %d %b %Y %H:%M:%S %z')
        if article_date >= previous_hour:
            _tweet_article(api, article)
    print('----- END -----')


if __name__ == '__main__':
    get_articles()
