from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet, base_name='users')

urlpatterns = [
    path('api/', include(router.urls)),
]
