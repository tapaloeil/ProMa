from django.contrib import admin
from .models import Environment,EnvironmentApps,EnvironmentData,SIEBEL_USERS
from jet.admin import CompactInline
# Register your models here.

class SIEBEL_USERSAdmin(admin.TabularInline):
    model=SIEBEL_USERS

class EnvironmentAppsAdmin(admin.TabularInline):
    model=EnvironmentApps

class EnvironmentDataAdmin(admin.TabularInline):
    model=EnvironmentData

class EnvironmentAdmin(admin.ModelAdmin):
    list_display=('id', 'Name', 'IP', 'DNS', 'MachineName')
    inlines=(EnvironmentDataAdmin,EnvironmentAppsAdmin,SIEBEL_USERSAdmin )


admin.site.register(Environment,EnvironmentAdmin)