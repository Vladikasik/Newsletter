import os
import django
import requests
from bs4 import BeautifulSoup
import time
from bot import Bot

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsLetter.settings")
django.setup()


from Parser.models import Article

class Head:

    def __init__(self):

        self.be_in_crypto_link = 'https://beincrypto.ru/news/'

    # parsing all articles and returning dict of them
    # to update them in db later
    def _parse_all_new(self):
        return self._be_in_crypto()

    # wrtiting recieved dict to db
    def write_all_articles(self):

        # receiving all new articles from parser
        all_new_articles_received = self._parse_all_new()

        # writing them in db by django.models
        for article_from_query in all_new_articles_received:
            if article_from_query["telegraph"] is not None:
                new_db_insert = Article(
                    article_title=article_from_query["title"],
                    article_text=article_from_query["html_text"],
                    article_link_telegraph=article_from_query["telegraph"],
                    article_link_to_origina_article=article_from_query["original_link"],
                    article_link_to_original_website=article_from_query["original_website"]

                )
                new_db_insert.save()

    # beincrypto.ru

    def _be_in_crypto(self):
        print('starting be on crypto')
        req = requests.get(self.be_in_crypto_link)
        soup = BeautifulSoup(req.text, 'html.parser')

        all_states = soup.findAll(
            'article',
            {"class": "multi-news-card bb-1 d-lg-flex flex-lg-column mb-5"})
        new_parsed = []
        for i in all_states:
            article = self._be_in_crypto_info(i)
            try:
                print(article['telegraph'])
                if article['title'] not in self._get_articles(self.be_in_crypto_link):
                    new_parsed.append(article)
            except:
                pass
        return new_parsed

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
                            if i.find('span'):
                                try:
                                    text = i.find('a').text
                                except:
                                    text = 'Error'
                                exit_text += text
                            else:
                                try:
                                    i['dir']
                                except:
                                    exit_text += str(i) + '\n'
                    elif i.name == 'h2':
                        exit_text += f"<h3>{i.text}</h3>\n"
                    elif i.name == 'figure':
                        img = i.find('amp-img')
                        if img:
                            img = f"<img src='{img['src']}'></img>"
                            exit_text += str(img) + '\n'
                    elif i.name == 'blockquote' and i.get('class') == 'wp-block-quote':
                        exit_text += str(i) + '\n'

                exit_text = pre_text + '\n<br>' +\
                    exit_text[pre_len + 8:]  # cutting pre-text
                return exit_text
            except Exception as ex:
                print('exeption in parse_article_content()')
                print(repr(ex))
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

        try:
            response = telegraph.create_page(
                str(title),
                html_content=str(text_state)
            )
            return 'https://telegra.ph/{}'.format(response['path'])
        except:
            print('error in telegreaph creating')


if __name__ == "__main__":
    parser = Head()
    while True:
        parser.write_all_articles()
        print('waiting 10 min')
        bot = Bot()
        bot.mailing_to_all()
        time.sleep(600)
