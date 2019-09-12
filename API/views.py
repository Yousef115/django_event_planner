from datetime import datetime
from django.contrib.auth.models import User


from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from events.models import Booking, Event, Profile
from .permissions import IsOwner
from .serializers import (EventsListSerializer, EventDetailsSerializer, CreateEventSerializer, 
							BookEventSerializer, BookingDetailsSerializer, UserSerializer, 
							RegisterSerializer, EventOwnerDetailSerializer)

#OK
class EventsList(ListAPIView):
	queryset = Event.objects.all()
	serializer_class = EventsListSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['owner__username']

	def get_queryset(self):
		today = datetime.today()
		return Event.objects.filter(date__gte=today)

#OK
class EventDetails(RetrieveAPIView):
	queryset = Event.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'

	def get_serializer_class(self):
		print (self.kwargs['event_id'])
		event = Event.objects.get(id=self.kwargs['event_id'])
		if self.request.user == event.owner:
			return EventOwnerDetailSerializer
		else:
			return EventDetailsSerializer

#OK
class CreateEvent(CreateAPIView):
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		today = datetime.today()
		serializer.save(owner=self.request.user,created_on=today)

#OK
class ModifyEvent(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = CreateEventSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated, IsOwner]


class BookingsList(ListAPIView):
	#queryset = Booking.objects.all()
	serializer_class = BookingDetailsSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		today = datetime.today()
		return Booking.objects.filter(owner=self.request.user)


#OK
class BookEvent(CreateAPIView):
	serializer_class = BookEventSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		print (self.request.user)
		serializer.save(owner=self.request.user, event_id=self.kwargs['event_id'])


class ModifyBooking(RetrieveUpdateAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookEventSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'	


class Profile(RetrieveAPIView):
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user

class Register(CreateAPIView):
	serializer_class = RegisterSerializer


# class Follow(RetrieveUpdateAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = CreateEventSerializer
# 	lookup_field = 'id'
# 	lookup_url_kwarg = 'user_id'
# 	permission_classes = [IsAuthenticated,]


# class following(CreateAPIView):
# 	serializer_class = FollowSerializer
# 	permission_classes = [IsAuthenticated]

# 	def perform_create(self, serializer):
# 		print (self.request.user)
# 		serializer.save(owner=self.request.user, event_id=self.kwargs['event_id'])
