from django.db import models

# Create your models here.
class User(models.Model):

    user_name = models.CharField("Имя", max_length=50)
    user_tlg = models.CharField("Имя", max_length=30)
    expiration_date = models.DateField()
