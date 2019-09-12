from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import ( EventsList, EventDetails, CreateEvent, ModifyEvent, BookingsList, BookEvent, ModifyBooking, Profile, Register)

urlpatterns = [
    path('register/', Register.as_view(), name="api-register"),
    path('login/', TokenObtainPairView.as_view(), name="api-login"),
    
    path('events/', EventsList.as_view(), name="api-event-list"),
    path('event/create/', CreateEvent.as_view(), name="api-create-event"),
    path('event/modify/<int:event_id>/', ModifyEvent.as_view(), name="api-modify-event"),
    path('event/<int:event_id>/details/', EventDetails.as_view(), name="api-event-detail"),
    #path('event/<int:event_id>/booked/', BookedUserDetails.as_view(), name="api-booked-detail"),
    path('event/<int:event_id>/book/', BookEvent.as_view(), name="api-book-event"),
	path('profile/', BookingsList.as_view(), name="api-profile"),

    




]


