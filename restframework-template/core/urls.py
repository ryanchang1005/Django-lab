from django.urls import path, include

from rest_framework import routers

from post.views.post import PostViewSet
from user.views.user import UserViewSet

router = routers.SimpleRouter()
router.register('user', UserViewSet, base_name='user')
router.register('post', PostViewSet, base_name='post')

urlpatterns = [
    path('api/', include(router.urls))
]
