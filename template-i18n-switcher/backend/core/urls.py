from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('home/', index, name='index'),
)
