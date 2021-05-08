from django.db import models
from django.conf import settings
from django.shortcuts import reverse

import markdown
import re


# Create your models here.

# 网站导航菜单栏分类表
class BigCategory(models.Model):
    # 导航名称
    name = models.CharField('一级分类', max_length=20)
    # 用作文章的访问路径，每篇文章有独一无二的标志，下同
    slug = models.SlugField(unique=True)
    # 分类页描述
    description = models.TextField('描述',
                                   max_length=240,
                                   default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')
    # 分类页Keywords
    keywords = models.TextField('关键字',
                                max_length=240,
                                default=settings.SITE_KEYWORDS,
                                help_text='用来作为SEO中keywords，长度参考SEO标准')

    class Meta:
        verbose_name = '一级分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 导航栏，分类下的下拉菜单分类
class Category(models.Model):
    # 分类名字
    name = models.CharField('二级分类', max_length=20)
    # slug 用作分类路径，独一无二
    slug = models.SlugField(unique=True)
    # 分类栏目页描述
    description = models.TextField('描述',
                                   max_length=240,
                                   default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')
    # 对应导航菜单外键
    bigcategory = models.ForeignKey(BigCategory, verbose_name='一级分类', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '二级分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category',
                       kwargs={'slug': self.slug,
                               'bigslug': self.bigcategory.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self)


# 文章标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述',
                                   max_length=240,
                                   default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag',
                       kwargs={'tag': self.name})

    def get_article_list(self):
        # 返回当前标签下所有发表的文章列表
        return Article.objects.filter(tags=self)


# 文章关键词，用来作为SEO中keywords
class Keyword(models.Model):
    name = models.CharField('文章关键词', max_length=20)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    # 文章默认略缩图
    IMG_LINK = 'surface.jpg'
    # 文章作者
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作者", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='文章标题')
    summary = models.TextField('文章摘要',
                               max_length=700,
                               default='文章摘要等同于网页description内容，请务必填写...')
    # 文章内容
    body = models.TextField(verbose_name='文章内容')
    img_link = models.CharField('图片地址', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('阅览量', default=0)
    loves = models.IntegerField('喜爱量', default=0)
    series_name = models.CharField(verbose_name='系列名称', default='none', max_length=20)
    # 文章唯一标识符
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, verbose_name='文章分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    keywords = models.ManyToManyField(Keyword,
                                      verbose_name='文章关键词',
                                      help_text='文章关键词，用来作为SEO中keywords,最好使用长尾词，3-4个足够')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'sulg': self.slug})

    def body_to_markdown(self):
        return markdown.markdown(self.body, extension=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_pre(self):
        return Article.objects.filter(id_lt=self.id).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id_gt=self.id).order_by('id').first()


# 公告
class Activate(models.Model):
    text = models.TextField('公告', null=True)
    is_active = models.BooleanField('是否开启', default=False)
    add_date = models.DateTimeField('提交日期', auto_now_add=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 幻灯片
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField('标题',
                             max_length=20,
                             blank=True,
                             null=True,
                             help_text='标题可以为空')
    content = models.CharField('描述', max_length=80)
    img_url = models.CharField('图片地址', max_length=200)
    url = models.CharField('跳转链接',
                           max_length=200,
                           default='#',
                           help_text='图片跳转的超链接，默认#表示不跳转')

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间越晚越靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]


# 友情链接表
class FriendLink(models.Model):
    name = models.CharField('网站名称', max_length=50)
    description = models.CharField('网站描述', max_length=100, blank=True)
    link = models.URLField('友链地址', help_text='请填写http或https开头的完整形式地址')
    logo = models.URLField('网站LOGO', help_text='请填写http或https开头的完整形式地址', blank=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否有效', default=True)
    is_show = models.BooleanField('是否首页展示', default=False)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name

    def get_home_url(self):
        # 提取友链的主页
        u = re.findall(r'(http|https://.*?)/.*?', self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=['is_show'])


# 图片标签
class AlbumTag(models.Model):
    name = models.CharField('图片标签', max_length=20)
    update_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    surface = models.ImageField(verbose_name='封面', default='default.jpg', upload_to='album/surface/')
    slug = models.SlugField(unique=True)
    description = models.TextField('描述',
                                   max_length=240,
                                   default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '图片标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:album_tag',
                       kwargs={'album_tag': self.name})

    def get_album_list(self):
        # 返回当前标签下所有发表的图片列表
        return Album.objects.filter(tags=self)


# 图片
class Album(models.Model):
    name = models.CharField(verbose_name='图片名称', default='无授权转载分享，请勿商用，侵删', max_length=20)
    tags = models.ManyToManyField(AlbumTag, verbose_name='图片标签')
    # 图片作者
    author = models.CharField(verbose_name="作者", default='佚名', max_length=20)
    # 图片内容
    picture = models.ImageField(verbose_name='图片', default='default.jpg', upload_to='album/')
    is_picture_title = models.BooleanField(verbose_name='是否为头版背景', default=False)
    title_tag = models.CharField(verbose_name='头版背景标签', default='', max_length=10)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('阅览量', default=0)
    loves = models.IntegerField('喜爱量', default=0)
    # 图片唯一标识符
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('blog:album', kwargs={'sulg': self.slug})

    def get_pre(self):
        return Album.objects.filter(id_lt=self.id).order_by('-id').first()

    def get_next(self):
        return Album.objects.filter(id_gt=self.id).order_by('id').first()


class GameInfo(models.Model):
    name = models.CharField(verbose_name='游戏名称', max_length=20)
    uid = models.IntegerField(verbose_name='UID')
    photo = models.ImageField(verbose_name='游戏信息截图')

    def __str__(self):
        return self.name


class Base(models.Model):
    hits = models.IntegerField(verbose_name='点击量')

    def __str__(self):
        return self.id
