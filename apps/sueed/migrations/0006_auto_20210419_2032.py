# Generated by Django 3.2 on 2021-04-19 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sueed', '0005_auto_20210418_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='albumtag',
            name='surface',
            field=models.ImageField(default='default.jpg', upload_to='', verbose_name='封面'),
        ),
        migrations.AlterField(
            model_name='albumtag',
            name='description',
            field=models.TextField(default='Sueedの小窝，记录生活瞬息，分享欢乐时光', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='bigcategory',
            name='description',
            field=models.TextField(default='Sueedの小窝，记录生活瞬息，分享欢乐时光', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='bigcategory',
            name='keywords',
            field=models.TextField(default='Sueed，个性，IT，游戏，二次创作，同人', help_text='用来作为SEO中keywords，长度参考SEO标准', max_length=240, verbose_name='关键字'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='Sueedの小窝，记录生活瞬息，分享欢乐时光', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.TextField(default='Sueedの小窝，记录生活瞬息，分享欢乐时光', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述'),
        ),
    ]
