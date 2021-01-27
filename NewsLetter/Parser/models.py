from django.db import models
# Create your models here.
class Article(models.Model):

    article_title = models.CharField("Название", max_length=100)
    article_text = models.TextField("Описание")
