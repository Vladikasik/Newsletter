# Generated by Django 3.1.4 on 2021-01-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0002_auto_20210128_0104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_name', models.CharField(max_length=20, verbose_name='Название сообщение')),
                ('message_text', models.TextField(verbose_name='Текст сообщения')),
            ],
        ),
    ]