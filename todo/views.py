#from django.http import HttpResponse, JsonResponse
#from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect
from .models import Todo
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from todo.serializers import TodoSerializer,UserSerializer,TodoShortSerializer
from rest_framework import status, generics, permissions
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

class api_create_todo(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = "scheduling/api_todo_create.html"

	def get(self, request, format=None):
		serializer = TodoShortSerializer()
		return Response({"serializer":serializer}, template_name='scheduling/api_todo_create.html')

	def post(self, request, format="None"):
		serializer=TodoShortSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(Owner=self.request.user)
			return redirect("tasklist")
		return redirect("tasklist")

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