import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from Project.models import Project
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField
from filer.fields.image import FilerImageField
from filer.fields.file  import FilerFileField
from model_utils.models import TimeStampedModel
from django.db.models.signals import pre_save
from django.utils.timezone import now

class TaskCategory(TimeStampedModel):
	Name=models.CharField(max_length=200, verbose_name=_("Category Name"))
	Description=HTMLField(blank=True,null=True, verbose_name=_("Description"))
	Project=models.ForeignKey(Project, verbose_name=_("Project Name"))

	def __str__(self):
		return self.Name

class TaskDomain(TimeStampedModel):
	Name=models.CharField(max_length=200, verbose_name=_("Domain Name"))
	Description=HTMLField(blank=True,null=True, verbose_name=_("Description"))
	Project=models.ForeignKey(Project, verbose_name=_("Project Name"))

	def __str__(self):
		return self.Name

class FuncProcess(TimeStampedModel):
	Name=models.CharField(max_length=300, verbose_name=_("Functional Processus"))
	Description=HTMLField(blank=True,null=True, verbose_name=_("Description"))
	Project=models.ForeignKey(Project, verbose_name=_("Project Name"))

	def __str__(self):
		return self.Name

class Task(TimeStampedModel):
	Project=models.ForeignKey(Project, verbose_name=_("Project Name"))
	Name=models.CharField(max_length=200, verbose_name=_("Task Name"))
	Description=HTMLField(blank=True,null=True, verbose_name=_("Description"))
	Category=models.ForeignKey(TaskCategory, verbose_name=_("Category"), related_name="tasks")
	Domain=models.ForeignKey(TaskDomain, verbose_name=_("Domain"), related_name="tasks")
	FuncProcess=models.ForeignKey(FuncProcess, verbose_name=_("FuncProcess"), blank=True, null=True, related_name="tasks")
	PlannedStart=models.DateTimeField(default=timezone.now, verbose_name=_("Planned Start"), null=True, blank=True)
	Baseline=models.DecimalField(decimal_places=2, max_digits=5,default=1, verbose_name=_("Baseline"))
	PlannedEnd=models.DateTimeField(verbose_name=_("Planned End"), null=True, blank=True )
	STATUS_CH=(
		("To Plan",_("To Plan")),
		("To Do",_("To Do")),
		("In Progress", _("In Progress")),
		("Done",_("Done")),
		)
	Status=models.CharField(max_length=30, choices=STATUS_CH, default="To Plan")
	AssignedTo=models.ForeignKey('auth.User',verbose_name=_("Assigned To"), related_name='tasks')
	COMPLEXITY_CH=(
		("1","Very Low"),
		("2","Low"),
		("3","Medium"),
		("4", "High"),
		("5","Very High"),
		)
	PRIORITY_CH=(
		("5","Very Low"),
		("4","Low"),
		("3","Medium"),
		("2", "High"),
		("1","Very High"),
		)
	Complexity=models.CharField(max_length=30, choices=COMPLEXITY_CH, default="2")
	Priority=models.CharField(max_length=30, choices=PRIORITY_CH, default="2")
	ActualStart=models.DateTimeField(blank=True,null=True)
	ActualEnd=models.DateTimeField(blank=True,null=True)
	Dependance=models.ManyToManyField("self", symmetrical=False, related_name="dependances+",blank=True)

	def __str__(self):
		return "%s - %s" % (self.pk,self.Name)


class TaskImage(TimeStampedModel):
	Task=models.ForeignKey(Task, related_name="images", verbose_name=_("Task"))
	Image=FilerImageField(related_name="task_image", null=True, blank=True, verbose_name=_("Image"))
	Description=models.CharField(max_length=200, blank=True, null=True)

class TaskFile(TimeStampedModel):
	Task=models.ForeignKey(Task, related_name="files", verbose_name=_("Task"))
	File=FilerFileField(related_name="task_file", null=True, blank=True, verbose_name=_("File"))
	Description=models.CharField(max_length=200, blank=True, null=True)	

