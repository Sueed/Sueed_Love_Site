# Generated by Django 3.2 on 2021-04-26 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sueed', '0013_article_series_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hits', models.IntegerField(verbose_name='点击量')),
            ],
        ),
    ]