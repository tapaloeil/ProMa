from django.contrib import admin
from .models import Project, User_X, EmployeeSchedule, NationalDayOffGroup, NationalDayOff, ExtraHolidays
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from jet.admin import CompactInline

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
	#list_filter=()
	#search_fields=["",]
	list_display=("Name","Slug","Client","Start","End","Active","Primary","tag_list","Administrator")
	#inlines=()
	#exclude=("Slug",)
	#js=[]
	fieldsets=(
		(None,{
			'fields':(("Name","Client"),"Description",("Start","End"), "Administrator")
			}),
		('Advanced',{
			'classes' : ('collapse',),
			'fields':(("Active","Primary", "Tags"),"Users"),
			}),
		)

	def get_queryset(self, request):
		return super(ProjectAdmin, self).get_queryset(request).prefetch_related('Tags')

	def tag_list(self, obj):
		return u", ".join(o.name for o in obj.Tags.all())

admin.site.register(Project, ProjectAdmin)

###################################

class ExtendedUserInline(admin.StackedInline):
    model = User_X
    can_delete = False
    verbose_name_plural = 'employee'
    required=True
    exclude=("Slug","")

class ExtraHolidaysInline(admin.TabularInline):
	model=ExtraHolidays

class UserAdmin(BaseUserAdmin):
	inlines=(ExtendedUserInline, ExtraHolidaysInline)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

###################################

class EmployeeScheduleAdmin(admin.ModelAdmin):
	list_display=("pk","name","monday","tuesday","wednesday","thursday","friday","saturday","sunday")
	list_editable=("name","monday","tuesday","wednesday","thursday","friday","saturday","sunday")

admin.site.register(EmployeeSchedule, EmployeeScheduleAdmin)

###################################

class NationalDayOffInline(admin.TabularInline):
	model=NationalDayOff

class NationalDayOffAdmin(admin.ModelAdmin):
	inlines=[NationalDayOffInline,]

admin.site.register(NationalDayOffGroup, NationalDayOffAdmin)