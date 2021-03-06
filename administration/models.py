from django.db import models
from django.contrib import admin
from django.utils import timezone

class Order(models.Model):
    Names  =   models.CharField(max_length=70)
    Last_names = models.CharField(max_length=70)
    Phone = models.CharField(max_length=50)
    Address = models.CharField(max_length=200)
    Reference = models.CharField(max_length=200,blank=True, null=True)
    states = (
    	('inactive', 'Inactive'),
	    ('check', 'Check'),
	    ('active', 'Active'),
	    ('complete', 'Complete'),
	    )
    State = models.CharField(
	    max_length=10,
	    choices=states,
	    default='check',
	    )
    Description =  models.CharField(max_length=200,blank=True, null=True)
    Note =  models.CharField(max_length=200,blank=True, null=True)
    Create = models.DateTimeField(default=timezone.now,blank=True, null=True)
    def __str__(self):
        return self.Names

class Type(models.Model):
    Name = models.CharField(max_length=50,unique=True)
    Descripcion = models.CharField(max_length=200)
    color = models.CharField(max_length=50,blank=True, null=True)
    Create = models.DateTimeField(blank=True, null=True)
    def publish(self):
    	self.Create = timezone.now()
    	self.save()
    def __str__(self):
        return '%s' % (self.Name)

class Service(models.Model):
	Order = models.ForeignKey(Order, on_delete=models.CASCADE)
	Type = models.ForeignKey(Type, on_delete=models.CASCADE)
	Description =  models.CharField(max_length=200)
	Note =  models.CharField(max_length=200,blank=True, null=True)
	states = (
		('Inactive', 'Inactive'),
		('Active', 'Active'),
		)
	State = models.CharField(
		max_length=10,
		choices=states,
		default='Active',
		)
	Create = models.DateTimeField(default=timezone.now,blank=True, null=True)
	def __str__(self):
		return '%s %s' % (self.Order, self.Type)
	class Meta:
		unique_together = (("Order", "Type"),)

class Profile(models.Model):
	Names  =   models.CharField(max_length=70)
	Last_names = models.CharField(max_length=70)
	IdPersonal = models.CharField(max_length=50)
	Phone = models.CharField(max_length=50)
	Address = models.CharField(max_length=200)
	Start_Work = models.DateTimeField(blank=True, null=True)
	states = (
		('inactive', 'Inactive'),
		('active', 'Active'),
		('register', 'register'),
		)
	State = models.CharField(
		max_length=10,
		choices=states,
		default='register',
		)
	Usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE,blank=True, null=True)
	Create = models.DateTimeField(default=timezone.now,blank=True, null=True)
	Note =  models.CharField(max_length=200,blank=True, null=True)
	def __str__(self):
		return '%s %s' % (self.Names, self.Last_names)

class Assign(models.Model):
	Service = models.ForeignKey(Service, on_delete=models.CASCADE,blank=True, null=True)
	Start_date = models.DateTimeField(blank=True, null=True)
	End_date = models.DateTimeField(blank=True, null=True)
	Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	Create = models.DateTimeField(default=timezone.now,blank=True, null=True)
	Note =  models.CharField(max_length=200,blank=True, null=True)
	states = (
		('assing', 'assing'),
		('active', 'Active'),
		)
	State = models.CharField(
		max_length=10,
		choices=states,
		default='assing',
		)
	def __str__(self):
		return '%s %s' % (self.Job, self.Profile)