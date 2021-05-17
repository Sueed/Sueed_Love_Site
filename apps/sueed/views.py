import re

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


# 判断是否手机端
def judge_pc_or_mobile(ua):
    """
    判断访问来源是pc端还是手机端
    :param ua: 访问来源头信息中的User-Agent字段内容
    :return:
    """
    factor = ua
    is_mobile = False
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp' \
                    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)' \
                    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)' \
                     r'|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)' \
                     r'|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw' \
                     r'|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8' \
                     r'|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit' \
                     r'|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)' \
                     r'|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji' \
                     r'|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx' \
                     r'|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi' \
                     r'|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)' \
                     r'|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg' \
                     r'|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21' \
                     r'|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-' \
                     r'|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it' \
                     r'|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)' \
                     r'|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)' \
                     r'|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit' \
                     r'|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'

    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(factor) != None:
        is_mobile = True
    user_agent = factor[0:4]
    if _short_matches.search(user_agent) != None:
        is_mobile = True

    return is_mobile


def IndexView(request):
    return render(request, 'index.html')


def HomeView(request):
    ua = request.META.get('HTTP_USER_AGENT')
    is_mobile = judge_pc_or_mobile(ua)
    return render(request, 'home.html', {'is_mobile': is_mobile})


def ArticleView(request):
    return render(request, 'article/article.html')


def AboutView(request):
    ua = request.META.get('HTTP_USER_AGENT')
    is_mobile = judge_pc_or_mobile(ua)
    return render(request, 'about.html', {'is_mobile': is_mobile})


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