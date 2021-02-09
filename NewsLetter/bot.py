import os
import django
import telebot
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsLetter.settings")
django.setup()

from Bot.models import Bot_message, Code, User
from Parser.models import Article

class Bot:

    def __init__(self):

        bot_token = "1550008254:AAGwdmlxuB2GnMnxnE79HD1DBmW_z6vh8iM"

        # bot_token = "1409431136:AAGiPb991cejge3vxLt9PkX4-2QTGsvvc_o" # my bot

        self.bot = telebot.TeleBot(bot_token)

    def mainloop(self):

        @self.bot.message_handler(commands=['start', 'preferences', 'help'])
        def main_commands(msg):

            self.bot.send_message(msg.chat.id, self._gm(msg))

        @self.bot.message_handler(commands=['code'])
        def main_commands(msg):

            # validatig promo
            def check_promo(msg, user_id):
                # recieving code if it exists
                promo = self._get_promo(msg.text)
                if promo:
                    user = self._get_user(user_id)
                    if user:
                        self.bot.send_message(
                            msg.chat.id, "Мы еще не доработали функционал для продления "
                            "подписки существующем пользователям, пожалуйста напиши "
                            "tlg-@vladislav_ain если у вас возникли проблемы")
                    else:
                        user_name = msg.from_user.first_name + ' ' + msg.from_user.last_name
                        user_id = msg.from_user.id
                        new_user = User(user_name=user_name,
                                        user_id_tlg=user_id,
                                        expiration_date=promo.promo_duration)
                        new_user.save()
                        promo.delete()
                else:
                    answer = self._gm('wrong_code')
                    self.bot.send_message(msg.chat.id, answer)

            # validating promo

            message_choose = self.bot.send_message(
                msg.chat.id, 'Отправьте ваш промокод')
            self.bot.register_next_step_handler(
                message_choose, check_promo, msg.from_user.id)

        self.bot.polling()

    # simply getting mesages from db
    def _gm(self, name):
        try:
            return Bot_message.objects.get(message_name=name.text).message_text
        except:
            return Bot_message.objects.get(message_name=name).message_text

    # get all promos
    def _get_promo(self, usr_msg):
        try:
            return Code.objects.get(code=int(usr_msg))
        except:
            return None

    # getting user if he exists
    def _get_user(self, usr_id):
        try:
            return User.objects.get(user_id_tlg=usr_id)
        except:
            return None

    def mailing_to_all(self):
        articles = Article.objects.filter(is_sent=False)
        now_date = datetime.datetime.now()
        all_active_user = User.objects.all()
        for article in articles:
            for user in all_active_user:
                if user.expiration_date >= now_date.date():
                    to_send = f"*{article.article_title}*\n[Читать]({article.article_link_to_origina_article})"
                    self.bot.send_message(
                        user.user_id_tlg, to_send, parse_mode='Markdown')
                    article.is_sent = True
                    article.save()


if __name__ == "__main__":
    bot = Bot()
    bot.mainloop()
