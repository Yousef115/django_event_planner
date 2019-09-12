from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save 
from django.contrib.auth.models import User

class Event(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE , related_name='created_events')
	title = models.CharField(max_length= 150)
	description = models.TextField()
	location = models.TextField()
	date = models.DateField()
	time = models.TimeField()
	seats = models.PositiveSmallIntegerField()
	# booked_seats = models.PositiveSmallIntegerField()
	created_on = models.DateTimeField(auto_now=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return (self.title)

	def get_absolute_url(self):
		return reverse('detail-event',kwargs={'event_id':self.id})

	def remaining_seats(self):
		booked_seats = self.bookings.all()
		total = 0
		for seat in booked_seats:
			total += seat.seats
		return  self.seats - total


class Booking(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE , related_name='booked_events')
	event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name='bookings')
	seats = models.PositiveSmallIntegerField()

	def __str__(self):
		return ("Owner: %s -------- Event: %s" %(self.owner, self.event))

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	following = models.ManyToManyField(User, blank=True, related_name='followers')
	followers = models.ManyToManyField(User, blank=True, related_name='following')
	bio = models.TextField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return str(self.user)


def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile.objects.create(user = instance)

post_save.connect(create_profile, sender = User)

