import smtplib
import os

GMAIL_ADDR = os.environ.get('GMAIL_ADDR')
GMAIL_PWD = os.environ.get('GMAIL_PWD')

sent_from = GMAIL_ADDR
to = [GMAIL_ADDR, 'onizuka1022@msn.com']
subject = 'A new article available on fatalement'


def _send_email(article):
  try:
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.ehlo()
      server.login(GMAIL_ADDR, GMAIL_PWD)
      
      body = f'Hey, \n A new article called {article.title} is availble\n\n read the article here {article.link}'

      email_text = """\
      From: %s
      To: %s
      Subject: %s

      %s
      """ % (sent_from, ", ".join(to), subject, body)
      
      server.sendmail(sent_from, to, email_text)
      server.close()

      print('Email sent!')
  except Exception as e:
      print(f'Something went wrong...: {e}')
    
def get_articles():
    previous_hour = datetime.today().replace(tzinfo=pytz.utc) - timedelta(hours=72)
    feed_url = "https://fatalement.com/feed.xml"
    blog_feed = feedparser.parse(feed_url)

    for article in blog_feed.entries:
        article_date = datetime.strptime(article.published, '%a, %d %b %Y %H:%M:%S %z')
        if article_date >= previous_hour:
            _send_email(article)
    print('----- END -----')


if __name__ == '__main__':
    get_articles()
