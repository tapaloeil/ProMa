import datetime
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
# Create your models here.

class Todo(models.Model):
	Owner=models.ForeignKey('auth.User',verbose_name=_("Owner"), related_name='todos')
	Description=models.CharField(max_length=2000)
	Created=models.DateTimeField(auto_now_add=True)
	Completed=models.DateTimeField(blank=True,null=True)
	Done=models.BooleanField(default=False)
	PRIORITY_CHOICES=( 
		('1', 'Low'),
	    ('2', 'Normal'),
	    ('3', 'High'),
	    ('4', 'Urgent')
	    )
	Priority=models.CharField(max_length=2,choices=PRIORITY_CHOICES, default="2")

	def get_priority_html_class(self):
		if self.Priority == '1':
			return "callout-info"
		if self.Priority == '2':
			return "callout-success"
		if self.Priority == '3':
			return "callout-warning"
		if self.Priority == '4':
			return "callout-danger"

	def __str__(self):
		return u'%s - %s' % (self.Owner.username, self.Description)

	def pre_save(sender, instance, *args, **kwargs):
		if instance.Done==True and instance.Completed==None:
			instance.Completed=datetime.now()
		if instance.Done==False and instance.Completed != None:
			instance.Completed=None	


pre_save.connect(Todo.pre_save, Todo)