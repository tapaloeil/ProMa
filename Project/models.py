import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from django.db.models.signals import pre_save, post_save, pre_delete, post_migrate
from django.utils.text import slugify
from model_utils import FieldTracker
from filer.fields.image import FilerImageField
from django.utils.translation import ugettext_lazy as _

#from allauth.account.adapter import DefaultAccountAdapter
#
#class MyAccountAdapter(DefaultAccountAdapter):    
#    def is_open_for_signup(self, request):
#        return False

class Project(models.Model):
	Name=models.CharField(max_length=200, verbose_name=_("Project Name"))
	Slug=models.SlugField(unique=True)
	Client=models.CharField(max_length=200, verbose_name=_("Client Name"))
	Description= HTMLField(blank=True,null=True, verbose_name=_("Description"))
	Start=models.DateField(default=datetime.date.today, verbose_name=_("Start"))
	End=models.DateField(blank=True,null=True, verbose_name=_("End"))
	Active=models.BooleanField(default=True, verbose_name=_("Active"))
	Primary=models.BooleanField(default=False, verbose_name=_("Primary"))
	Tags=TaggableManager(blank=True, verbose_name=_("Tags"))
	Photo=FilerImageField(related_name="project_image", null=True, blank=True, verbose_name=_("Photo"))
	Administrator=models.ForeignKey('auth.User', verbose_name=_("Administrator"))
	Users = models.ManyToManyField(User, blank=True, related_name="Project_Users", verbose_name=_("Users"))
	tracker = FieldTracker()


	class Meta:
		verbose_name=_("Project")
		verbose_name_plural=_("Projects")

	def __str__(self):
		return self.Name

def create_slug(instance, new_slug=None):
    slug=slugify(instance.Name)
    if new_slug is not None:
        slug=new_slug
    qs=Project.objects.filter(Slug=slug).order_by("-id")
    exists=qs.exists()
    if(exists):
        new_slug="%s-%s" % (slug, str(uuid.uuid4())[:12])
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_Project_receiver(sender, instance, *args, **kwargs):
    if not instance.Slug or instance.tracker.has_changed("Name"):
        instance.Slug=create_slug(instance)
    if instance.Primary==True:
    	qs=Project.objects.filter(Primary=True)
    	exists=qs.exists()
    	for e in qs:
    		e.Primary=False
    		e.save()
    else:
    	if int(Project.objects.filter(Primary=True).count()) == 0:
    		instance.Primary=True

def pre_delete_Project_receiver(sender, instance, *args, **kwargs):
	if instance.Primary == True:
		qs=Project.objects.filter(Primary=False)
		exists=qs.exists()
		if exists:
			rec=qs.first()
			rec.Primary=True
			rec.save()

pre_delete.connect(pre_delete_Project_receiver, sender=Project)
pre_save.connect(pre_save_Project_receiver, sender=Project)

############################################################

class ExtraHolidays(models.Model):
	User=models.ForeignKey(User)
	Start=models.DateField(verbose_name=_("Start"))
	End=models.DateField(blank=True,null=True, verbose_name=_("End"))
	NbDays=models.DecimalField(max_digits=4,decimal_places=1,verbose_name=_("Nb Days"))
	STATUS_CH=(
		("Planned", _("Planned")),
		("Registered",_("Registered")),
		)
	Status=models.CharField(max_length=30, choices=STATUS_CH, default="Planned")

	def __str__(self):
		return u"%s | %s - %s" % (seld.User.username,self.Start, self.End)


############################################################

class NationalDayOffGroup(models.Model):
	name=models.CharField(max_length=50, default="default")

	def __str__(self):
		return self.name

class NationalDayOff(models.Model):
	group=models.ForeignKey(NationalDayOffGroup)
	dayoffdate=models.DateField(verbose_name=_("Date"))

	def __str__(self):
		return '%s' % (self.dayoffdate)

###########################################################

class EmployeeSchedule(models.Model):
	name=models.CharField(default="40",max_length=20,verbose_name=_("Name"))
	monday=models.DecimalField(default="8.0",max_digits=10,decimal_places=2,verbose_name=_("Monday"))
	tuesday=models.DecimalField(default="8.0",max_digits=10,decimal_places=2,verbose_name=_("Tuesday"))
	wednesday=models.DecimalField(default="8.0",max_digits=10,decimal_places=2,verbose_name=_("Wednesday"))
	thursday=models.DecimalField(default="8.0",max_digits=10,decimal_places=2,verbose_name=_("Thursday"))
	friday=models.DecimalField(default="8.0",max_digits=10,decimal_places=2,verbose_name=_("Friday"))
	saturday=models.DecimalField(default="0.0",max_digits=10,decimal_places=2,verbose_name=_("Saturday"))
	sunday=models.DecimalField(default="0.0",max_digits=10,decimal_places=2,verbose_name=_("Sunday"))

	def __str__(self):
		return self.name

##########################################################

class User_X(models.Model):
	User=models.OneToOneField(User)
	Slug=models.SlugField(unique=True)
	CompanyName=models.CharField(max_length=200,default="Accenture",verbose_name=_("Company Name"))
	CurrentRole=models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Current Role"))
	ScheduleUser=models.ForeignKey(EmployeeSchedule, verbose_name=_("Schedule"))
	DayOffGroup=models.ForeignKey(NationalDayOffGroup, verbose_name=_("National Day Off Group"), null=True, blank=True)

def create_slug_User(instance, new_slug=None):
    slug=slugify(instance.username)
    if new_slug is not None:
        slug=new_slug
    qs=User_X.objects.filter(Slug=slug).order_by("-id")
    exists=qs.exists()
    if(exists):
        new_slug="%s-%s" % (slug, str(uuid.uuid4())[:12])
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_UserX_receiver(sender, instance, *args, **kwargs):
	if not instance.Slug:
		instance.Slug=create_slug_User(instance.User)
	if not hasattr(instance,'ScheduleUser'):
		rec=EmployeeSchedule.objects.all()
		if not rec.exists():
			EmployeeSchedule.objects.create(name="40")
		instance.ScheduleUser=EmployeeSchedule.objects.all().first()
	if not instance.DayOffGroup:
		rec=None
		rec=NationalDayOffGroup.objects.all()
		if not rec.exists():
			print("no group 2")
			NationalDayOffGroup.objects.create(name="default")
		instance.DayOffGroup=NationalDayOffGroup.objects.all().first()
	if not hasattr(instance,'DayOffGroup'):
		print("no group")
		rec=None
		rec=NationalDayOffGroup.objects.all()
		if not rec.exists():
			print("no group 2")
			NationalDayOffGroup.objects.create(name="default")
		instance.DayOffGroup=NationalDayOffGroup.objects.all().first()

def post_save_User_receiver(sender, instance, *args, **kwargs):
	rec=User_X.objects.filter(User=instance)
	exists=rec.exists()
	if not exists:
		User_X.objects.create(User=instance)
		
pre_save.connect(pre_save_UserX_receiver, sender=User_X)
post_save.connect(post_save_User_receiver, sender=User)

