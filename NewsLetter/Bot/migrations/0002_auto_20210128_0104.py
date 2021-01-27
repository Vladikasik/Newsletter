# Generated by Django 3.1.4 on 2021-01-27 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_promocode',
            field=models.CharField(default=0, max_length=10, verbose_name='Промокод пользователя на подписку'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='expiration_date',
            field=models.DateField(verbose_name='Дата окончания срока подписки'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_tlg',
            field=models.CharField(max_length=30, verbose_name='Ник в телеграм'),
        ),
    ]
