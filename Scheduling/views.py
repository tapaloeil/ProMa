from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import TaskSerializer
from .models import Task
from django.db.models import Sum, F, Q

def tasklist(request):
	tasks = Task.objects.filter(Status="To Plan")
	return render(request, 'scheduling/tasklist.html', {"tasks":tasks})

def taskgraph(request):
	return render(request, 'scheduling/taskgraph.html', {})

def taskgantt(request):
	return render(request, 'scheduling/taskgantt.html', {})

class api_tasklist(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

class api_taskgraph(APIView):
	def get(self, request, format=None):
		data=request.GET
		data_filter=request.GET.get('data_filter', None)
		if data_filter is not None:
			tasks=Task.objects.filter(~Q(Status=data_filter)).values(data_t=F(data["col"])).annotate(sum=Sum('Baseline'))
		else:
			tasks=Task.objects.values(data_t=F(data["col"])).annotate(sum=Sum('Baseline'))
		return Response(tasks)