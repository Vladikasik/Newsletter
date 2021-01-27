from django.db import models
# Create your models here.
class Article(models.Model):

    article_title = models.CharField("Название", max_length=100)
    article_text = models.TextField("Текст статьи в html")
    article_link_telegraph = models.URLField("Ссылка на статью в telegra.ph")
    article_link_to_original = models.URLField(
        "Ссылка оригинала статьи, или на наш сайт.")
