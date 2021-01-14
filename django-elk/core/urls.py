from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('info/', info),
    path('error/', error),
]
