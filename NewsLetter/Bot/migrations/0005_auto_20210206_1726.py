# Generated by Django 3.1.4 on 2021-02-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0004_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='promo_duration',
            field=models.DateField(verbose_name='Время промокода'),
        ),
    ]