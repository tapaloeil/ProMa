from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.renderers import TemplateHTMLRenderer,HTMLFormRenderer
from .serializers import TaskDepSer,TaskShortSerializer,TaskSerializer, Gantt_TaskCategory_Serializer, Gantt_Task_Update_Serializer
from .models import Task, FuncProcess
from django.db.models import Sum, F, Q, Min, Max, Count
from django.http import Http404

def taskdashboard(request):
	d=dict()
	all_domain = Task.objects.values(data_t=F("Domain__Name")).annotate(min_d=Min("PlannedStart"), max_d=Max("PlannedStart"), sum_d=Sum("Baseline"))
	all_category = Task.objects.values(data_t=F("Category__Name")).annotate(min_d=Min("PlannedStart"), max_d=Max("PlannedStart"), sum_d=Sum("Baseline"))
	all_funcprocess = Task.objects.values(data_t=F("FuncProcess__Name")).annotate(min_d=Min("PlannedStart"), max_d=Max("PlannedStart"), sum_d=Sum("Baseline"))
	all_overall = Task.objects.aggregate(min_d=Min("PlannedStart"), max_d=Max("PlannedStart"), sum_d=Sum("Baseline"), count_d=Count("pk"))

	rep_domain = Task.objects.values(data_t=F("Domain__Name"), data_s=F("Status")).annotate(min_d=Min("PlannedStart"), max_d=Max("PlannedStart"), sum_d=Sum("Baseline"))
	rep_category = Task.objects.values(data_t=F("Category__Name"), data_s=F("Status")).annotate(min_d=Min("PlannedStart"), max_d=Max("PlannedStart"), sum_d=Sum("Baseline"))
	rep_funcprocess = Task.objects.values(data_t=F("FuncProcess__Name"), data_s=F("Status")).annotate(min_d=Min("PlannedStart"), max_d=Max("PlannedStart"), sum_d=Sum("Baseline"))
	rep_status = Task.objects.values(data_s=F("Status")).annotate(sum_d=Sum("Baseline"), count_d=Count("pk"))

	return render(request, "scheduling/dashboard.html", 
		{
		"all_domain":all_domain,
		"all_category":all_category,
		"all_funcprocess":all_funcprocess,
		"all_overall":all_overall,
		"rep_domain":rep_domain,
		"rep_category":rep_category,
		"rep_funcprocess":rep_funcprocess,
		"rep_status":rep_status,
		})

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

class api_gantt_task(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = FuncProcess.objects.all()#filter(pk__in=[25])
	serializer_class = Gantt_TaskCategory_Serializer

class api_gantt_task_update(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset=Task.objects.all()
	serializer_class=Gantt_Task_Update_Serializer

class api_gantt_task_dependance(generics.RetrieveUpdateDestroyAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	queryset = Task.objects.all()
	serializer_class = TaskDepSer

class api_taskCreate (APIView):
	renderer_classes = [TemplateHTMLRenderer,HTMLFormRenderer]
	template_name = "scheduling/api_task_create.html"

	def get(self, request, format=None):
		serializer = TaskShortSerializer()
		return Response({"serializer":serializer}, template_name='scheduling/api_task_create.html')

	def post(self, request, format="None"):
		serializer=TaskShortSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return redirect("tasklist")
		return redirect("tasklist")

class api_taskDetail (APIView):
	renderer_classes = [TemplateHTMLRenderer,HTMLFormRenderer]
	template_name = "scheduling/api_task_form.html"

	def get_object(self,pk):
		try:
			return Task.objects.get(pk=pk)
		except Task.DoesNotExist:
			raise Http404

	def get (self, request, pk, format=None):
		task=self.get_object(pk)
		serializer = TaskShortSerializer(task)
		return Response({"serializer":serializer, "task":task})

	def post (self, request, pk, format=None):
		task=self.get_object(pk)
		serializer=TaskShortSerializer(task,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return redirect("tasklist")
		return redirect("tasklist")

	#def post(self, request, format=None):
	#	serializer=TaskSerializer(data=request.data)
	#	if serializer.is_valid():
	#		serializer.save()
	#		return Response({"serializer":serializer})
	#	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
