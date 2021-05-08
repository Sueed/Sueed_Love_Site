from django.conf.urls import url
from django.urls import path, re_path
from django.views.static import serve

from .views import IndexView, HomeView, ArticleView, AboutView, ContactView, ApiView, AlbumTagView, TagDetailView, ArticleDetailView, ErrorView, EmailView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(r'', IndexView, name='index'),

    path(r'send_email/', EmailView, name='email'),

    path(r'404/', ErrorView, name='404'),

    path(r'home/', HomeView, name='home'),

    path(r'album/', AlbumTagView, name='album_tag'),

    re_path(r'^album/(?P<tag_slug>.*?)/$', TagDetailView, name='pictures'),

    path(r'article/', ArticleView, name='article'),

    re_path(r'^article/(?P<tag_slug>.*?)/$', ArticleDetailView, name='pictures'),

    path(r'about/', AboutView, name='about'),

    path(r'connect/', ContactView, name='contact'),

    path(r'contact/', AlbumTagView, name='album'),

    re_path(r'^contact/(?P<slug>.*?)/$', AlbumTagView, name='album'),

    path(r'api/census/button-render/', ApiView, name='api'),
    path(r'api/census/form-render/', ApiView, name='api'),
    path(r'api/1/performance/records/', ApiView, name='api'),
    path(r'api/1/performance/settings/', ApiView, name='api'),
    path(r'api/census/RecordHit', ApiView, name='api'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
