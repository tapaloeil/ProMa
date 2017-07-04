from django.conf.urls import url
from . import views
from .views import api_get_todo_list,api_create_todo

urlpatterns=[
	url(r'^$', views.get_todo_list, name='todo_list'),
	url(r'^api/list/$', api_get_todo_list.as_view(), name="api_get_todo_list"),
	url(r'^api/detail/(?P<pk>[0-9]+)/$',views.TodoDetail.as_view(), name="api_todo_detail"),
	url(r'^api/listcreate/$', views.TodoList.as_view(), name="api_todo_list"),
	url(r'^api/users/$', views.UserList.as_view()),
	url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
	url(r'^api/create/$', api_create_todo.as_view(), name="api_create_todo"),
]