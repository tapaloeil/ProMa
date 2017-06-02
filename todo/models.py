import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Todo_Group(models.Model):
	Owner=models.ForeignKey('auth.User', verbose_name=_("Owner"))
	Name=models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Group Name"))
	Collapse=models.BooleanField(default=False, verbose_name=_("Collapse ?"))

	def __str__(self):
		return u'%s - %s' % (self.Owner.username, self.Name)

class Todo(models.Model):
	Group=models.ForeignKey(Todo_Group)
	Description=models.CharField(max_length=2000)
	Created=models.DateTimeField(auto_now_add=True)
	Completed=models.DateTimeField(blank=True,null=True)
	Done=models.BooleanField(default=False)
	PRIORITY_CHOICES=( 
		('1', '1'),
	    ('2', '2'),
	    ('3', '3'),
	    )
	Priority=models.CharField(max_length=2,choices=PRIORITY_CHOICES, default="2")

	def __str__(self):
		return u'%s - %s' % (self.Group.Name, self.Description)