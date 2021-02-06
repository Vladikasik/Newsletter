from django.db import models

# Create your models here.
class User(models.Model):

    user_name = models.CharField("Имя", max_length=50)
    user_id_tlg = models.CharField("Ник в телеграм", max_length=30)
    expiration_date = models.DateField("Дата окончания срока подписки")

    def __str__(self):
        return self.user_name

class Bot_message(models.Model):

    message_name = models.CharField("Название сообщение", max_length=20)
    message_text = models.TextField("Текст сообщения")

    def __str__(self):
        return self.message_name

class Code(models.Model):

    code = models.IntegerField('Промокод пользователя на подписку')
    promo_duration = models.DateField('Время промокода')

    def __str__(self):
        return str(self.code)
