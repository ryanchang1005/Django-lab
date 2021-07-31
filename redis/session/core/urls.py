from django.contrib import admin
from django.urls import path
from rest_framework import routers

from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
]

router = routers.SimpleRouter()

urlpatterns += router.urls
