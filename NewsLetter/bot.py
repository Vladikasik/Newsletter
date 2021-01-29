import os
import django
import telebot

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsLetter.settings")
django.setup()

from Bot.models import Bot_message


class Bot:

    def __init__(self):

        bot_token = "1550008254:AAGwdmlxuB2GnMnxnE79HD1DBmW_z6vh8iM"

        self.bot = telebot.TeleBot(bot_token)

        self.messages = Bot_message

    def mainloop(self):

        @self.bot.message_handler(commands=['start'])
        def main_commands(msg):

            self.bot.send_message(msg.chat.id, self._gm(msg))

        self.bot.polling()

    # simply getting mesages from db
    def _gm(self, name):
        try:
            return self.messages.objects.get(message_name=name.text).message_text
        except:
            return self.messages.objects.get(message_name=name).message_text


if __name__ == "__main__":
    bot = Bot()
    bot.mainloop()
