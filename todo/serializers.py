from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
	get_priority_html_class=serializers.ReadOnlyField()
	Owner=serializers.ReadOnlyField(source='Owner.username')

	class Meta:
		model = Todo
		fields = ('id', 'Owner', 'Description', 'Completed', 'Done', 'Priority', 'get_priority_html_class')


	def create(self, validated_data):
		return Todo.objects.create(**validated_data)

	def update(self,instance,validated_data):
		instance.Description=validated_data.get('Description', instance.Description)
		instance.Done=validated_data.get('Done', instance.Done)
		instance.Priority=validated_data.get('Priority', instance.Priority)
		instance.save()
		return instance


from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	todos=serializers.PrimaryKeyRelatedField(many=True, queryset=Todo.objects.all())

	class Meta:
		model=User
		fields=('id', 'username', 'todos')