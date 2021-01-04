from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from post.views.post import PostViewSet
from user.views.user import UserViewSet

router = routers.SimpleRouter()
router.register('user', UserViewSet, base_name='user')
router.register('post', PostViewSet, base_name='post')

urlpatterns = [
    path('api/', include(router.urls))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
