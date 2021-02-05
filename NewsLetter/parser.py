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
            print(article['telegraph'])
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

                # getting ready state to parse
                main_div = soup.find('div', {"class": "entry-content-inner"})
                pre_div = main_div.find(
                    'div', {"class": "intro-text"})
                pre_text = pre_div.findAll('p')[1].text
                pre_len = len(str(pre_div.findAll('p')[1]))
                pre_text = f'<strong>"{pre_text}"</strong>'
                exit_text = ''

                # parsing and translating to telegraph tags
                for i in main_div.findAll({'p': True, 'h2': True, 'figure': True, 'blockquote': True}):
                    if i.name == 'p':
                        if i.find('amp-ad'):
                            pass
                        else:
                            exit_text += str(i) + '\n'
                    elif i.name == 'h2':
                        exit_text += f"<h3>{i.text}</h3>\n"
                    elif i.name == 'figure':
                        img = i.find('amp-img')
                        img = f"<img src='{img['src']}'></img>"
                        exit_text += str(img) + '\n'
                    elif i.name == 'blockquote':
                        exit_text += str(i) + '\n'

                exit_text = pre_text + '\n' +\
                    exit_text[pre_len + 8:]  # cutting pre-text
                return exit_text
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
        main_text = parse_article_content(article_link)
        result_article_html = article_image + main_text
        telegraph_link = self._write_state(article_title, result_article_html)
        to_return = {'title': article_title,
                     'html_text': result_article_html,
                     'telegraph': telegraph_link,
                     'original_link': article_link,
                     'original_website': self.be_in_crypto_link}
        print(to_return)
        return to_return

    # getting list of all articles to see if new were written
    def _get_articles(self, link):
        to_return = Article.objects.filter(
            article_link_to_original_website=link).values_list('article_title', flat=True)
        # to_return = to_return.article_title.all()
        return to_return

    # write telegraph and get link
    def _write_state(self, title, text_state):
        from telegraph import Telegraph

        telegraph = Telegraph()

        telegraph.create_account(short_name='1337')

        response = telegraph.create_page(
            str(title),
            html_content=str(text_state)
        )

        return 'https://telegra.ph/{}'.format(response['path'])


if __name__ == "__main__":
    parser = Head()
    print(parser._be_in_crypto())
