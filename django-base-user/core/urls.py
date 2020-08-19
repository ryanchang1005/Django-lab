from django.contrib import admin
from django.urls import path
from rest_framework import routers
from users.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
]

router = routers.SimpleRouter()
router.register('users', UserViewSet, base_name='user')

urlpatterns += router.urls
