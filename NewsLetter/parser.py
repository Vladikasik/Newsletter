import os
import django
import requests
from bs4 import BeautifulSoup
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsLetter.settings")
django.setup()


from Parser.models import Article

class Head:

    def __init__(self):

        self.be_in_crypto_link = 'https://beincrypto.ru/news/'

    # parsing all articles and returning dict of them
    # to update them in db later
    def _parse_all_new(self):
        return []

    # wrtiting recieved dict to db
    def write_all_articles(self):

        # receiving all new articles from parser
        all_new_articles_received = self._parse_all_new(self)

        # writing them in db by django.models
        for article_from_query in all_new_articles_received:
            new_db_insert = Article(
                article_title=article_from_query["title"],
                article_text=article_from_query["text"]
            )
            new_db_insert.save()

    # beincrypto.ru
    def _be_in_crypto(self)
        pass
