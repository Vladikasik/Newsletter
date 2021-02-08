# Generated by Django 3.1.4 on 2021-02-05 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parser', '0002_auto_20210128_0104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article_link_to_original',
            new_name='article_link_to_origina_article',
        ),
        migrations.AddField(
            model_name='article',
            name='article_link_to_original_website',
            field=models.URLField(default='', verbose_name='Ссылка на сайт с которого был произведен парсинг'),
            preserve_default=False,
        ),
    ]