from django.contrib import admin
from .models import FuncProcess,TaskCategory,TaskDomain,Task, TaskFile, TaskImage
from django import forms
from django.forms.models import ModelForm
from jet.admin import CompactInline
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
# Register your models here.


class TaskImageInline(CompactInline):
	model=TaskImage

class TaskFileInline(CompactInline):
	model=TaskFile

#class TaskAdminForm(forms.ModelForm):
#	def clean_PlannedStart(self):
#		print("updatePlannedEnd")


class TaskImportExport(resources.ModelResource):
	class Meta:
		model = Task
		fields = ('id', 'Name', 'Category__Name', 'Domain__Name','FuncProcess__Name',"PlannedStart",'Baseline', 'Complexity', 'Priority', 'Dependance', "AssignedTo__username" )
		export_order = ('id', 'Name', 'Category__Name','Domain__Name','FuncProcess__Name',"PlannedStart",'Baseline', 'Complexity', 'Priority', 'Dependance', "AssignedTo__username")


class TaskAdmin(ImportExportActionModelAdmin):
	resource_class = TaskImportExport
	view_on_site = False
	#form = TaskAdminForm
	list_display=('id','Name', 'Category', 'Domain', 'Baseline', "Complexity", "Priority")
	list_filter=('Category__Name', 'Domain__Name', 'FuncProcess__Name', "Status" )
	search_fields=["Name"]
	list_editable=('Baseline','Complexity','Priority')
	fieldsets=(
		(None,{
			'fields':(('Name'), ('Category', 'Domain', 'FuncProcess'), ("PlannedStart","Baseline"), ("Complexity", "Priority"), 'Project'),
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
			'FuncProcess': self.getLastCreatedTaskValue("FuncProcess"),
			'Category': self.getLastCreatedTaskValue("Category"),
			'Domain': self.getLastCreatedTaskValue("Domain"),
			'Project': self.getLastCreatedTaskValue("Project"),
			'Complexity': self.getLastCreatedTaskValue("Complexity"),
			'Priority': self.getLastCreatedTaskValue("Priority"),
			'AssignedTo': self.getLastCreatedTaskValue("AssignedTo"),
			 }

admin.site.register(FuncProcess)
admin.site.register(TaskCategory)
admin.site.register(TaskDomain)
admin.site.register(Task, TaskAdmin)


