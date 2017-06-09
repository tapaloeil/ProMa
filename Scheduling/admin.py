from django.contrib import admin
from .models import TaskCategory,TaskDomain,Task, TaskFile, TaskImage
from django import forms
from django.forms.models import ModelForm
from jet.admin import CompactInline
# Register your models here.


class TaskImageInline(CompactInline):
	model=TaskImage

class TaskFileInline(CompactInline):
	model=TaskFile

class TaskAdminForm(forms.ModelForm):
	def clean_PlannedStart(self):
		print("updatePlannedEnd")



class TaskAdmin(admin.ModelAdmin):
	view_on_site = False
	form = TaskAdminForm
	list_display=('Name', 'Category', 'Domain', 'Project', "Status", "PlannedStart", "Complexity", "Priority")
	list_filter=('Category__Name', 'Domain__Name', "Project__Name", "Status", "PlannedStart", "Complexity", "Priority" )
	search_fields=["Name"]
	fieldsets=(
		(None,{
			'fields':('Name', ('Category', 'Domain', 'Project'), ("PlannedStart","Baseline"), ("Complexity", "Priority")),
			}),
		('Description',{
			'fields':("Description",),
			}),
		('Advanced',{
			'classes' : ('collapse',),
			'fields':("Status","PlannedEnd","AssignedTo","ActualStart","ActualEnd","Dependance"),
			}),
		)
	inlines=(TaskFileInline,TaskImageInline)

	def getLastCreatedTaskValue(self, field):
		try:
			qs=Task.objects.latest("created")
			return getattr(qs, field)
		except :
			return ""			

	def get_changeform_initial_data(self, request):
		return {
			'Category': self.getLastCreatedTaskValue("Category"),
			'Domain': self.getLastCreatedTaskValue("Domain"),
			'Project': self.getLastCreatedTaskValue("Project"),
			'Complexity': self.getLastCreatedTaskValue("Complexity"),
			'Priority': self.getLastCreatedTaskValue("Priority"),
			'AssignedTo': self.getLastCreatedTaskValue("AssignedTo"),
			 }

admin.site.register(TaskCategory)
admin.site.register(TaskDomain)
admin.site.register(Task, TaskAdmin)