from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
# ------------------------
__author__ = 'sueed'
__date__ = '2021/4/10 22:16'

# ------------------------

from django.shortcuts import render
from .models import Article, Base


def TagDetailView(request, tag_slug):
    return render(request, 'album/pictures.html', {'tag_slug': tag_slug})


def ArticleDetailView(request, tag_slug):
    article_list = Article.objects.filter(id=tag_slug)
    return render(request, 'article/article_detail.html', {'article': article_list[0]})


def AlbumTagView(request):
    return render(request, 'album/album.html')


def ApiView(request):
    # 处理api接口处理
    if request.method == 'GET':
        return JsonResponse({"isConfigurationLoaded": True, "experimentContextList": [
            {"name": "ab", "experimentType": "AB_TEST", "segmentName": "default", "variant": "true",
             "containsError": True, "status": "INACTIVE"},
            {"name": "v7-user-sites-app-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"},
            {"name": "commerce-cart-app-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"},
            {"name": "resource-plugin-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "false", "containsError": False, "status": "ACTIVE"},
            {"name": "v7_1-user-sites-app-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"},
            {"name": "squarespace-app-app-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "false", "containsError": False, "status": "ACTIVE"},
            {"name": "browser-tests-app-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"},
            {"name": "page_speed-plugin-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"},
            {"name": "api-endpoint-rollout", "experimentType": "AB_TEST", "segmentName": "default", "variant": "false",
             "containsError": True, "status": "INACTIVE"},
            {"name": "rum", "experimentType": "FEATURE_TOGGLE", "segmentName": "default", "variant": "true",
             "containsError": False, "status": "ACTIVE"},
            {"name": "campaigns-app-rollout", "experimentType": "AB_TEST", "segmentName": "default", "variant": "true",
             "containsError": False, "status": "ACTIVE"},
            {"name": "performance-dashboard-app-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "false", "containsError": False, "status": "ACTIVE"},
            {"name": "demo-app-rollout", "experimentType": "AB_TEST", "segmentName": "default", "variant": "true",
             "containsError": False, "status": "ACTIVE"},
            {"name": "v7_1-config-app-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"},
            {"name": "v7-config-app-rollout", "experimentType": "AB_TEST", "segmentName": "default", "variant": "true",
             "containsError": False, "status": "ACTIVE"},
            {"name": "track-user-timing-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"},
            {"name": "commerce-checkout-app-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"},
            {"name": "rum-rollout", "experimentType": "AB_TEST", "segmentName": "default", "variant": "true",
             "containsError": False, "status": "ACTIVE"},
            {"name": "user-plugin-rollout", "experimentType": "AB_TEST", "segmentName": "default", "variant": "true",
             "containsError": False, "status": "ACTIVE"},
            {"name": "track-page-speed-rollout", "experimentType": "AB_TEST", "segmentName": "default",
             "variant": "true", "containsError": False, "status": "ACTIVE"}],
                             "pageLoadId": "ee593ff2-ac30-40e1-b42d-6d8cd20efa3c"}, safe=False)
    elif request.method == 'POST':
        hit_number = Base.objects.get(id=1).hits
        Base.objects.filter(id=1).update(hits=hit_number + 1)
        return JsonResponse('', safe=False)


def IndexView(request):
    return render(request, 'index.html')


def HomeView(request):
    return render(request, 'home.html')


def ArticleView(request):
    return render(request, 'article/article.html')


def AboutView(request):
    return render(request, 'about.html')


def ContactView(request):
    return render(request, 'contact.html')


def ErrorView(request):
    return render(request, '404.html')


def EmailView(request):
    if request.method == 'POST':
        send_email(request)
    else:
        return render(request, '403.html')


class SendEmail(forms.Form):
    first_name = forms.CharField(min_length=2, widget=widgets.TextInput(attrs={'class': 'form-control'}),
                                 label='姓', error_messages={'required': "Name 名字 is missing required subfields: First"})
    lst_name = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}),
                               label='名', error_messages={'required': "Name 名字 is missing required subfields: Last"})
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'class': 'form-control'}),
                             label='邮箱', error_messages={'required': "Email Address 电邮 is required.",
                                                         'invalid': 'Email Address 电邮 is not '
                                                                    'valid. Email addresses '
                                                                    'should follow the format '
                                                                    'user@domain.com.'})
    subject = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}),
                              label='确认密码', error_messages={'required': "Subject 题 is required."})
    messages = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}),
                               label='确认密码', error_messages={'required': "Message 讯息 （提问、邀请、意见） is required."})


def send_email(request):
    form = SendEmail(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # Users.objects.create(**form.cleaned_data)
    else:
        print(form.cleaned_data)
        errors = form.errors
        return render(request, 'contact.html', locals())

    return HttpResponse('ok')
