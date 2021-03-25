from django.urls import path

from core.views import *

urlpatterns = [
    path('', index, name='index'),
    path('short_url/create/', create, name='create'),
    path('short_url/<slug:code>/', detail, name='detail'),

    # 錯誤
    path('404/', handle404, name='handle404'),

    # 導向
    path('<slug:code>/', redirect, name='redirect'),
]
