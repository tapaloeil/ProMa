from django.conf.urls import url
from . import views
from django.contrib import admin
from .views import api_tasklist,api_taskgraph
from rest_framework import routers

routers=routers.DefaultRouter()

urlpatterns=[
	url(r'^$', views.tasklist, name='tasklist'),
    url(r'^graph/$', views.taskgraph, name='taskgraph'),
    url(r'^gantt/$', views.taskgantt, name='taskgantt'),
	url(r'^api/list/$', api_tasklist.as_view(), name="api_tasklist"),
    url(r'^api/graph/$', api_taskgraph.as_view(),name="api_taskgraph"),
]