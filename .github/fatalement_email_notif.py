from datetime import datetime, timedelta
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import feedparser
import pytz

GMAIL_ADDR = os.environ.get('GMAIL_ADDR')
GMAIL_PWD = os.environ.get('GMAIL_PWD')


def _send_email(article):
  sent_from = GMAIL_ADDR
  to = [GMAIL_ADDR, 'onizuka1022@msn.com']
  subject = 'A new article available on Fatalement.com'

  try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(GMAIL_ADDR, GMAIL_PWD)

    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADDR
    msg['To'] = ", ".join(to)
    msg['Subject'] = subject

    body = f"Hey, \n\nA new article called {article.title} is available! \nRead the article here {article.link} \n\nThanks a lot for reading the blog.\n\nDiane"
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()

    server.sendmail(sent_from, to, text)
    server.close()

    print('Email sent!')
  except Exception as e:
    print(f'Something went wrong...: {e}')
    
def get_articles():
    previous_hour = datetime.today().replace(tzinfo=pytz.utc) - timedelta(hours=2)
    feed_url = "https://fatalement.com/feed.xml"
    if hasattr(ssl, '_create_unverified_context'):
      ssl._create_default_https_context = ssl._create_unverified_context
    blog_feed = feedparser.parse(feed_url)

    for article in blog_feed.entries:
        article_date = datetime.strptime(article.published, '%a, %d %b %Y %H:%M:%S %z')
        if article_date >= previous_hour:
            _send_email(article)
    print('----- END -----')


if __name__ == '__main__':
    get_articles()
