from django.db import models

# Create your models here.
class User(models.Model):

    user_name = models.CharField("Имя", max_length=50)
    user_tlg = models.CharField("Ник в телеграм", max_length=30)
    expiration_date = models.DateField("Дата окончания срока подписки")
    user_promocode = models.CharField(
        "Промокод пользователя на подписку", max_length=10)

class Bot_message(models.Model):

    message_name = models.CharField("Название сообщение", max_length=20)
    message_text = models.TextField("Текст сообщения")
