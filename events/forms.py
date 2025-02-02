from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking, Profile

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class DateInput(forms.DateInput):
  input_type = 'date'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner', ]

        widgets={
        'date': DateInput(),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats']
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['following', 'bio', 'image']
    