import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from django.db.models.signals import pre_save
from django.utils.timezone import now

class Environment(TimeStampedModel):
	Name=models.CharField(max_length=200, verbose_name=_("Environment Name"))
	IP = models.GenericIPAddressField(protocol="both", verbose_name=_("IP Address"))
	DNS = models.CharField(max_length=300, verbose_name=_("DNS"))
	MachineName = models.CharField(max_length=200, verbose_name=_("Machine Name"))

	def __str__(self):
		return self.Name

class EnvironmentData(TimeStampedModel):
	Environment=models.ForeignKey(Environment, verbose_name=_("Environment Name"))
	Key=models.CharField(max_length=200, verbose_name=_("Key"))
	Value=models.CharField(max_length=200, verbose_name=_("Value"))

	def __str__(self):
		return "%s - %s:%s" % (self.Environment,self.Key,self.Value)

class EnvironmentApps(TimeStampedModel):
	Environment=models.ForeignKey(Environment, verbose_name=_("Environment Name"))
	Name=models.CharField(max_length=200, verbose_name=_("Application Name"))
	USE_CHOICES=(
		("IP",_("IP")),
		("DNS",_("DNS")),
		("MachineName", _("MachineName")),
		)
	UseIpMachineDNS=models.CharField(max_length=30, choices=USE_CHOICES, default="MachineName")
	URLCompletion=models.CharField(max_length=300, verbose_name=_("URL Completion"))

class SIEBEL_USERS(TimeStampedModel):
	EnvironmentApp=models.ForeignKey(EnvironmentApps, verbose_name=_("Application Name"))
	Environment=models.ForeignKey(Environment, verbose_name=_("Environment Name"),blank=True,null=True)
	User=models.CharField(max_length=200, verbose_name=_("Username"))
	Password=models.CharField(max_length=200, verbose_name=_("Password"))