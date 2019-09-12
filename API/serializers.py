from datetime import datetime
from django.contrib.auth.models import User



from rest_framework import serializers

from events.models import Event, Booking, Profile


class EventsListSerializer(serializers.ModelSerializer):
	description = serializers.HyperlinkedIdentityField(
		view_name = "api-event-detail",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)
	class Meta:
		model = Event
		fields = ['title', 'description']


class PastBookingDetailsSerializer(serializers.ModelSerializer):
	owner = serializers.StringRelatedField()
	class Meta:
		model = Event
		fields = ['owner', 'seats',]

	# def get_booking_owner(self, obj):
	# 	return obj.owner


class EventDetailsSerializer(serializers.ModelSerializer):
	owner = serializers.SerializerMethodField()
	book = serializers.HyperlinkedIdentityField(
		view_name = "api-book-event",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)
	class Meta:
		model = Event
		fields = ["title", "owner", "description", "location", "date", "time", 
		"seats", "book",]

	def get_owner(self, obj):
		return "%s"%(obj.owner.username)
	

class EventOwnerDetailSerializer(serializers.ModelSerializer):
	owner = serializers.SerializerMethodField()
	book = serializers.HyperlinkedIdentityField(
		view_name = "api-book-event",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)
	Attendees = serializers.SerializerMethodField() 
	class Meta:
		model = Event
		fields = ["title", "owner", "description", "location", "date", "time", 
		"seats", "book", "Attendees",]

	def get_owner(self, obj):
		return "%s"%(obj.owner.username)
	
	def get_Attendees(self, obj):
		bookings = obj.bookings.all()
		print ("\n\n Bookings: ", bookings)
		return PastBookingDetailsSerializer(bookings, many=True).data

class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ["title", "description", "date", "time", "location", "seats", ]

class BookEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['seats']


class BookingDetailsSerializer(serializers.ModelSerializer):
	event_owner = serializers.SerializerMethodField()
	event = EventsListSerializer()
	class Meta:
		model = Booking
		fields = ['event_owner', "event", "seats",]

	def get_event_owner(self, obj):
		return "%s "%(obj.event.owner.username)
		return "OK"



class UserSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	past_bookings = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ["username", "name", "email", "past_bookings"]

	def get_name(self, obj):
		return "%s %s"%(obj.first_name, obj.last_name)

	def get_past_bookings(self, obj):
		today = datetime.today()
		bookings = Booking.objects.filter(owner_username__contains=(obj))
		return PastBookingDetailsSerializer(bookings, many=True).data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data


# class FollowSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Profile
# 		fields = ['following']
