import random

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

# 首頁, 輸入URL
from shorturl.models import ShortURL
from shorturl.services import ShortURLService


@require_http_methods(['GET'])
def index(request):
    return HttpResponseRedirect(reverse('create'))


# 顯示輸入的URL的短網址
@require_http_methods(['GET'])
def detail(request, code):
    short_url = get_object_or_404(ShortURL, code=code)
    return render(request, 'citadel/detail.html', {
        'code': short_url.code,
        'url': short_url.url,
    })


# 產生短連結
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'GET':
        return render(request, 'citadel/create.html')
    else:
        url = request.POST.get('url')

        # retry 3 次
        cnt = 3
        while cnt > 0:
            try:
                it = ShortURL()
                it.code = generate_code()
                it.url = url
                it.save()
                return HttpResponseRedirect(reverse('detail', kwargs={'code': it.code}))
            except Exception as e:
                print(str(e))
                messages.error(request, '新增失敗')
                cnt -= 1
        return HttpResponseRedirect(reverse('index'))


def generate_code():
    """
    回傳一個由62種字串組成長度為7的字串
    """
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return ''.join([chars[random.randint(0, len(chars) - 1)] for _ in range(7)])


# 重新導向
@require_http_methods(['GET'])
def redirect(request, code):
    val = ShortURLService.get_url_with_cache(code)
    url = val['url']
    if not url:
        return HttpResponseRedirect(reverse('handle404'))
    return HttpResponseRedirect(url)


# 頁面找不到, 404頁面
@require_http_methods(['GET'])
def handle404(request):
    return render(request, 'citadel/404_error_page.html')
