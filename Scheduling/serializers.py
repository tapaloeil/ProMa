from rest_framework import serializers
from .models import Task


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