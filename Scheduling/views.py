from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import TaskSerializer
from .models import Task

def tasklist(request):
	tasks = Task.objects.filter(Status="To Plan")
	return render(request, 'scheduling/tasklist.html', {"tasks":tasks})

class api_tasklist(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Task.objects.all()
	serializer_class = TaskSerializer