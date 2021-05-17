# 创建了新的tags标签文件后必须重启服务器
import os

from django import template
from django.shortcuts import get_object_or_404

from ..models import Article, Category, Tag, Carousel, FriendLink, BigCategory, Activate, Keyword, AlbumTag, Album
from django.db.models.aggregates import Count
from django.utils.html import mark_safe
from PIL import Image

# 注册自定义标签函数
register = template.Library()

# 获取文章信息
@register.simple_tag
def get_article_all():
    return Article.objects.all().order_by('id')


# 获取文章详情
@register.simple_tag
def get_article_detail(article_id):
    return Article.objects.filter(id=article_id)

# 获取所有图片标签
@register.simple_tag
def get_album_tags():
    return AlbumTag.objects.all()


# 获取特定图片标签
@register.simple_tag
def get_detail_album_tag(tag_id):
    return AlbumTag.objects.filter(slug=tag_id)


# 获取图片详情
@register.simple_tag
def get_detail_album(tag_slug):
    if tag_slug:
        tag = get_object_or_404(AlbumTag, slug=tag_slug)
        album_list = Album.objects.filter(tags=tag).order_by('-id')
        return album_list


# 获取图片尺寸
@register.simple_tag
def get_picture_size(item, target):
    path = os.path.join(os.getcwd(), target + str(item))
    img = Image.open(path)
    size = img.size
    return str(size[0])+"x"+str(size[1])


# 获取二维码图片
@register.simple_tag
def get_contact_image():
    return Album.objects.filter(tags=8)


# 获取导航条大分类查询集
@register.simple_tag
def get_bigcategory_list():
    '''返回大分类列表'''
    return BigCategory.objects.all()


# 返回文章分类查询集
@register.simple_tag
def get_category_list(id):
    '''返回小分类列表'''
    return Category.objects.filter(bigcategory_id=id)


# 获取滚动的大幻灯片查询集、获取左侧的幻灯片查询集，这两个部分用的图片是一样的
@register.simple_tag
def get_carousel_index():
    return Carousel.objects.filter(number__lte=5)


# 获取热门排行数据查询集，参数：sort 文章类型，num 数量
# 文章相关标签函数，和热门文章使用同一个函数
@register.simple_tag
def get_article_list(sort=None, num=None):
    '''获取指定排序方式和指定数量的文章'''
    if sort:
        if num:
            return Article.objects.order_by(sort)[:num]
        return Article.objects.order_by(sort)
    if num:
        return Article.objects.all()[:num]
    return Article.objects.all()


# 获取右侧栏热门专题幻灯片查询集
@register.simple_tag
def get_carousel_right():
    return Carousel.objects.filter(number__gt=5, number__lte=10)


# 获取归档文章查询集
@register.simple_tag
def get_data_date():
    '''获取文章发表的不同月份'''
    article_dates = Article.objects.datetimes('create_date', 'month', order='DESC')
    return article_dates


# 获取文章标签信息，参数文章ID
@register.simple_tag
def get_article_tag(article_id):
    return Tag.objects.filter(article=article_id)


# 返回标签查询集
@register.simple_tag
def get_tag_list():
    """返回标签列表"""
    return Tag.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)


# 返回活跃的友情链接查询集
@register.simple_tag
def get_friends():
    """获取活跃的友情链接"""
    return FriendLink.objects.filter(is_show=True, is_active=True)


# 获取标题
@register.simple_tag
def get_title(category):
    a = BigCategory.objects.filter(slug=category)
    if a:
        return a[0]


# 获取文章详情页下方的推荐阅读文章
@register.simple_tag
def get_category_article():
    article_4 = get_article_list('views', 4)
    article_8 = get_article_list('views', 8)
    return {'article_4': article_4, 'article_8': article_8}


# 获取文章 keywords
@register.simple_tag
def get_article_keywords(article):
    keywords = []
    keys = Keyword.objects.filter(article=article)
    for key in keys:
        keywords.append(key.name)
    return ','.join(keywords)


# 获取前一篇文章，参数当前文章 ID
@register.simple_tag
def get_article_previous(article_id):
    has_previous = False
    id_previous = int(article_id) - 1
    while not has_previous and id_previous >= 1:
        article_previous = Article.objects.filter(id=id_previous)
        if not article_previous:
            id_previous -= 1
        else:
            has_previous = True
    if has_previous:
        article = Article.objects.filter(id=id_previous)[0]
        return article
    else:
        return


# 获取下一篇文章，参数当前文章ID
@register.simple_tag
def get_article_next(article_id):
    has_next = False
    id_next = int(article_id) + 1
    article_id_max = Article.objects.order_by('-id')[0]
    id_max = article_id_max.id
    while not has_next and id_next <= id_max:
        article_next = Article.objects.filter(id=id_next)
        if not article_next:
            id_next += 1
        else:
            has_next = True
    if has_next:
        article = Article.objects.filter(id=id_next)[0]
        return article
    else:
        return


# 返回公告查询集
@register.simple_tag
def get_active():
    """"获取活跃的友情链接"""
    text = Activate.objects.filter(is_active=True)
    if text:
        text = text[0].text
    else:
        text = ''
    return mark_safe(text)


@register.simple_tag
def my_highlight(text, q):
    """自定义标题搜索词高亮函数，忽略大小写"""
    if len(q) > 1:
        try:
            text = re.sub(q, lambda a: '<span class="highlighted">{}</span>'.format(a.group()),
                          text, flags=re.IGNORECASE)
            text = mark_safe(text)
        except:
            pass
    return text
