from django.conf.urls import url
from . import views
from django.contrib import admin
from .views import api_tasklist
from rest_framework import routers

routers=routers.DefaultRouter()

urlpatterns=[
	url(r'^$', views.tasklist, name='tasklist'),
	url(r'^api/list/$', api_tasklist.as_view(), name="api_tasklist"),
]