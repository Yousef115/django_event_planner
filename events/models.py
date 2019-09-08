from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	owner = models.ForeignKey(User, on_delete= models.CASCADE , related_name='created_events')
	title = models.CharField(max_length= 150)
	description = models.TextField()
	location = models.TextField()
	datetime = models.DateTimeField()
	seats = models.PositiveSmallIntegerField()
	created_on = models.DateTimeField(auto_now=True)
