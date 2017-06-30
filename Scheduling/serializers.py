from rest_framework import serializers
from rest_framework.fields import DictField,CharField
from .models import Task, FuncProcess
from django.db.models import Case, When
from datetime import date,datetime,timedelta
from django.utils import timezone
from rest_framework_recursive.fields import RecursiveField
from bdateutil import relativedelta

class TaskDepSer(serializers.ModelSerializer):
	class Meta:
		model=Task
		fields=('id','Dependance')

	def update(self, instance, validated_data):
		instance.Dependance=validated_data.get("Dependance", instance.Dependance)
		instance.save()
		return instance

class TaskShortSerializer(serializers.ModelSerializer):
	class Meta:
		model=Task
		fields = (
			'id',
			'Project', 
			'Name', 
			'Category', 
			'Domain', 
			'PlannedStart', 
			'Baseline',
			'AssignedTo',
			'Complexity',
			'Priority',
			)
	def create(self, validated_data):
		return Task.objects.create(**validated_data)

	def update(self,instance,validated_data):
		instance.Project=validated_data.get('Project', instance.Project)		
		instance.Name=validated_data.get('Name', instance.Name)
		instance.Category=validated_data.get('Category', instance.Category)
		instance.Domain=validated_data.get('Domain', instance.Domain)
		instance.PlannedStart=validated_data.get('PlannedStart', instance.PlannedStart)
		instance.Baseline=validated_data.get('Baseline', instance.Baseline)
		instance.AssignedTo=validated_data.get('AssignedTo', instance.AssignedTo)
		instance.Complexity=validated_data.get('Complexity', instance.Complexity)
		instance.Priority=validated_data.get('Priority', instance.Priority)
		instance.save()
		return instance	

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model=Task
		fields = (
			'id',
			'Project', 
			'Name', 
			'Description', 
			'Category', 
			'Domain', 
			'PlannedStart', 
			'Baseline',
			'PlannedEnd',
			'Status',
			'AssignedTo',
			'Complexity',
			'Priority',
			'ActualStart',
			'ActualEnd'
			)
	def create(self, validated_data):
		return Task.objects.create(**validated_data)

	def update(self,instance,validated_data):
		instance.Project=validated_data.get('Project', instance.Project)		
		instance.Name=validated_data.get('Name', instance.Name)
		instance.Description=validated_data.get('Description', instance.Description)
		instance.Category=validated_data.get('Category', instance.Category)
		instance.Domain=validated_data.get('Domain', instance.Domain)
		instance.PlannedStart=validated_data.get('PlannedStart', instance.PlannedStart)
		instance.PlannedEnd=validated_data.get('PlannedEnd', instance.PlannedEnd)
		instance.Baseline=validated_data.get('Baseline', instance.Baseline)
		instance.Status=validated_data.get('Status', instance.Status)
		instance.AssignedTo=validated_data.get('AssignedTo', instance.AssignedTo)
		instance.Complexity=validated_data.get('Complexity', instance.Complexity)
		instance.ActualStart=validated_data.get('ActualStart', instance.ActualStart)
		instance.ActualEnd=validated_data.get('ActualEnd', instance.ActualEnd)
		instance.Priority=validated_data.get('Priority', instance.Priority)
		instance.save()
		return instance

class Gantt_Task_Serializer(serializers.ModelSerializer):
	name = serializers.CharField(source='Name')
	_from = serializers.SerializerMethodField()
	color = serializers.SerializerMethodField()
	to = serializers.SerializerMethodField()

	class Meta:
		model=Task
		fields=(
			'id',
			'name',
			'_from',
			'to',
			'color',
			'Dependance',
			)
	def get__from(self, obj):
		if obj.PlannedStart is None:
			dd=date.today()
			return datetime(dd.year,dd.month,dd.day,10,0,0)
		else:
			return obj.PlannedStart

	def get_to(self, obj):
		if obj.PlannedStart is None :
			dd=date.today()
			tbdays=relativedelta(bdays=+int(round(obj.Baseline,0)-1))
			tlastday=timedelta(hours= 0)
			if int(round(obj.Baseline,0)) >= 1:
				tlastday=timedelta(hours= 8)
			tremaining=timedelta(hours=int(round((obj.Baseline % 1) * 8,0)))
			tEnd=datetime(dd.year,dd.month,dd.day,10,0,0)+tbdays+tlastday+tremaining
		else:
			tbdays=relativedelta(bdays=+int(round(obj.Baseline,0)-1))
			tremaining=timedelta(hours=int(round((obj.Baseline % 1) * 8,0)))
			tlastday=timedelta(hours= 0)
			if int(round(obj.Baseline,0)) >= 1:
				tlastday=timedelta(hours= 8)
			tEnd=obj.PlannedStart+tbdays+tlastday+tremaining
			#duration= tEnd - datetime(dd.year,dd.month,dd.day,9,0)
			
			#if duration.seconds//3600 > 4:
			#	tEnd=tEnd+timedelta(hours=1)
		return tEnd

	def get_color(self, obj):
		if obj.Domain.Name == "Siebel":
			return "#9FC5F8"
		if obj.Domain.Name == "BIP":
			return "#3C8CF8"
		if obj.Domain.Name == "OPA":
			return "#93C47D"
		if obj.Domain.Name == "Batch Siebel":
			return "#F1C232"
		else:
			return "#3C8CF8"


class Gantt_Task_Update_Serializer(serializers.ModelSerializer):
	class Meta:
		model=Task
		fields=(
			'id',
			'PlannedStart',
			'PlannedEnd',
		)
	
	def update(self, instance, validated_data):
		print(validated_data)
		instance.PlannedStart=validated_data["PlannedStart"]
		#instance.PlannedEnd=validated_data["PlannedEnd"]
		instance.save()
		return instance

class Gantt_TaskCategory_Serializer(serializers.ModelSerializer):
	name=serializers.CharField(source='Name')
	tasks = Gantt_Task_Serializer(many=True, read_only=True)
	class Meta:
		model=FuncProcess
		fields=(
			'name',
			'tasks'
			)