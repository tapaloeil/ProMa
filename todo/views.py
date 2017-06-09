#from django.http import HttpResponse, JsonResponse
#from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
#from django.views.generic import RedirectView
#from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
#from rest_framework.parsers import JSONParser
from rest_framework import status
from todo.serializers import TodoSerializer,UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwner
# Create your views here.

def get_todo_list(request):
	return render(request, "todo/todo.html", {"todo":Todo.objects.filter(Owner=request.user, Done=False).order_by('-Priority')})


class api_get_todo_list(APIView):
	renderer_classes=[TemplateHTMLRenderer]
	permission_classes = (permissions.IsAuthenticated,)
	template_name="todo/todo.html"

	def get(self, request, format=None):
		data=request.GET
		todo=Todo.objects.filter(Owner=request.user).order_by('-Priority')
		if data.get("option")!= "all":
			DoneFilter=True
			if data.get("option")=="active":
				DoneFilter=False
			todo=todo.filter(Done=DoneFilter)
		serializer=TodoSerializer(todo, many=True)
		return Response({'todo':serializer.data})


class TodoList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer

	def perform_create(self, serializer):
		serializer.save(Owner=self.request.user)


class TodoDetail(generics.RetrieveUpdateDestroyAPIView, IsOwner,):
	permission_classes = (permissions.IsAuthenticated,)
	queryset=Todo.objects.all()
	serializer_class=TodoSerializer


class UserList(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset=User.objects.all()
	serializer_class=UserSerializer


class UserDetail(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = User.objects.all()
	serializer_class = UserSerializer