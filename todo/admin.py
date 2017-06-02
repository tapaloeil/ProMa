from django.contrib import admin
from .models import Todo_Group, Todo
# Register your models here.

class TodoInline(admin.TabularInline):
	model=Todo

class TodoGroupAdmin(admin.ModelAdmin):
	inlines=(TodoInline, )

admin.site.register(Todo_Group,TodoGroupAdmin)
