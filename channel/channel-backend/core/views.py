from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

# 首頁, 聊天室列表
from chats.models import Chat
from core.utils.datetime import get_locale_str_by_utc_datetime_obj


# 聊天室列表
@require_http_methods(['GET'])
def index(request):
    chat_list = []
    for chat in Chat.objects.all():
        chat_list.append({
            'pub_id': chat.pub_id,
            'create_time': get_locale_str_by_utc_datetime_obj(chat.create_time),
        })
    return render(request, 'citadel/index.html', {
        'chat_list': chat_list,
    })


# 聊天室
@require_http_methods(['GET'])
def chat_room(request, pub_id):
    chat = get_object_or_404(Chat, pub_id=pub_id)
    return render(request, 'citadel/chat_room.html')


# 聊天室
@require_http_methods(['POST'])
def add_chat(request):
    print('add_chat')
    # 直接產生一個聊天室
    Chat().save()
    return HttpResponseRedirect(reverse('index'))
