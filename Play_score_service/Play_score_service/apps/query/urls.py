from django.conf.urls import url, include
from django.contrib import admin
from . import views
from query import views
urlpatterns = [
    url('', views.UsernameCountView, name='user'),
    url('upload/', views.Upload, name='upload'),
    url('show/', views.Show, name='show'),
]
