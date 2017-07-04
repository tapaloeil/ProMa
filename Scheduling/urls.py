from django.conf.urls import url
from . import views
from django.contrib import admin
from .views import api_tasklist,api_taskgraph,api_gantt_task,api_gantt_task_update,api_gantt_task_dependance, api_taskDetail,api_taskCreate
from rest_framework import routers

routers=routers.DefaultRouter()

urlpatterns=[
	url(r'^list/$', views.tasklist, name='tasklist'),
	url(r'^dashboard/$', views.taskdashboard, name="taskdashboard"),
    url(r'^graph/$', views.taskgraph, name='taskgraph'),
    url(r'^gantt/$', views.taskgantt, name='taskgantt'),
    url(r'^calendar/$', views.taskcalendar, name='taskcalendar'),
	url(r'^api/list/$', api_tasklist.as_view(), name="api_tasklist"),
	url(r'^api/create/$', api_taskCreate.as_view(), name="api_taskCreate"),
	url(r'^api/detail/(?P<pk>[0-9]+)/$',api_taskDetail.as_view(), name="api_taskDetail"),
    url(r'^api/graph/$', api_taskgraph.as_view(),name="api_taskgraph"),
    url(r'^api/gantt/$', api_gantt_task.as_view(), name='api_gantt_task'),
    url(r'^api/gantt/detail/(?P<pk>[0-9]+)/$', api_gantt_task_update.as_view(), name='api_gantt_task_update'),
    url(r'^api/gantt/dep/(?P<pk>[0-9]+)/$', api_gantt_task_dependance.as_view(), name='api_gantt_task_dependance'),
]