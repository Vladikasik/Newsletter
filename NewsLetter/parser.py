import os
import django
import requests
from bs4 import BeautifulSoup
import time
import telegraph

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

    # making article in telegraph
    def telegraph_link(self):
        pass

    # beincrypto.ru

    def _be_in_crypto(self):
        req = requests.get(self.be_in_crypto_link)
        soup = BeautifulSoup(req.text, 'html.parser')

        all_states = soup.findAll(
            'article',
            {"class": "multi-news-card bb-1 d-lg-flex flex-lg-column mb-5"})
        new_parsed = []
        for i in all_states:
            article = self._be_in_crypto_info(i)
            break
            # if article['title'] not in self._get_articles(self.be_in_crypto_link):
            #     new_parsed.append(article)

    # parsing all info for each article

    def _be_in_crypto_info(self, article):
        #
        #
        def parse_article_content(link):
            try:
                req = requests.get(link)
                soup = BeautifulSoup(req.text, "html.parser")
                main_div = soup.find('div', {"class": "entry-content-inner"})
                pre_div = main_div.find(
                    'div', {"class": "intro-text"})
                pre_text = pre_div.findAll('p')[1].text
                pre_text = f'<strong>"{pre_text}"</strong>'
                exit_text = ''
                for i in main_div.findAll({'p': True, 'h2': True, 'figure': True, 'blockquote': True}):
                    if i.name == 'p':
                        if i.find('amp-ad'):
                            print('add found')
                        else:
                            exit_text += str(i) + '\n'
                    elif i.name == 'h2':
                        exit_text += f"<h3>{i.text}</h3>\n"
                    elif i.name == 'figure':
                        exit_text += "<h3>Картинка)</h3>\n"
                    elif i.name == 'blockquote':
                        exit_text += str(i) + '\n'
                print(exit_text)
            except Exception as ex:
                print(ex)
                time.sleep(3)
                return parse_article_content(link)
        #
        #
        article_title = article.find('h3').find('a').text
        article_image_link = article.find('amp-img')['src']
        article_image = f"<img src='{article_image_link}'></img>"
        article_link = article.find('a')['href']
        parse_article_content(
            'https://beincrypto.ru/v-chikago-snimut-film-o-protivostoyanii-kriptovalyut-i-mira-uoll-strit/')

        print(article_link)
        print()
        print()

        to_return = {'title': article_title, 'original_link': article_link}

        return to_return

    # getting list of all articles to see if new were written
    def _get_articles(self, link):
        to_return = Article.objects.filter(
            article_link_to_original_website=link).values_list('article_title', flat=True)
        # to_return = to_return.article_title.all()
        return to_return


if __name__ == "__main__":
    parser = Head()
    parser._be_in_crypto()
