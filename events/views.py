from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from django.views import View
from .models import Event, Booking, Profile
from .forms import UserSignup, UserLogin , EventForm, BookingForm, ProfileForm

class Home(View):
    form_class = BookingForm
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(date__gte = timezone.now())
        query = request.GET.get("q")
        if query:
            events = Event.objects.filter(
            Q(date__gte = timezone.now()),
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(owner__username__icontains=query)
            ).distinct()
        form = self.form_class()
        context = {
            'events' : events,
            'form' : form,
        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        event_obj = Event.objects.get(id = kwargs['event_id'])
        form = self.form_class(request.POST)

        if int(request.POST['seats']) > event_obj.remaining_seats():
            messages.warning(request, "You requested more than remaining seats!")
            return redirect('home')
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = request.user
            booking.event = event_obj
            booking.save()
            messages.warning(request, "Your seats have been booked!")

        return redirect('dashboard')
    
class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect ('home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


def dashboard(request):
    booked = request.user.booked_events.filter(event__date__gte=timezone.now())
    past_books = request.user.booked_events.filter(event__date__lt=timezone.now())
    organized_events = request.user.created_events.all()
    context = {
        'organized_events': organized_events,
        'booked_events': booked,
        'past_books': past_books
    }
    return render(request, 'dashboard.html', context)


def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.owner = request.user
            user.save()
            return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'create_event.html', context)


class EventDetail(View):
    form_class = BookingForm
    template_name = 'event_detail.html'

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id = kwargs['event_id'])
        bookings = Booking.objects.filter(event=event)
        form = self.form_class()
        context = {
            'event': event,
            'form': form,
        }
        return render(request, self.template_name, context)

    # DRY = Don't Repeat Yourself
    def post(self, request, *args, **kwargs):
        event_obj = Event.objects.get(id = kwargs['event_id'])
        form = self.form_class(request.POST)

        if int(request.POST['seats']) > event_obj.remaining_seats():
            messages.warning(request, "You requested more than remaining seats!")
            return redirect('home')
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = request.user
            booking.event = event_obj
            booking.save()
            messages.success(request, "Your seats have been booked!")
            
        return redirect('dashboard')



def edit_event(request, event_id):
    event_obj = Event.objects.get(id = event_id)
    if request.user != event_obj.owner:
        return redirect('home') # rude
    form= EventForm(instance = event_obj)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form': form,
        'event': event_obj,
    }
    return render(request, 'edit_event.html', context)


def follow(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    # user is the organizer profile to be followed
    user = User.objects.get(id=user_id)
    # logged_user is the user who wants to follow the organizer 
    logged_user = request.user
    user.save()
    # add the organizer to logged in users following list
    logged_user.profile.following.add(user)
    # add logged in user to the organizer follower list
    user.profile.followers.add(logged_user)
    msg = "You have followed %s" %(user.username)
    messages.success(request, msg)
    return redirect ('dashboard')

class UserProfile(View):
   template_name = 'profile.html'
   def get(self, request, *args, **kwargs):
        the_user = User.objects.get(id = kwargs['user_id'])
        followers = the_user.profile.followers.count()
        following = the_user.profile.following.count()
        context = {
           'user': the_user,
           'followers': followers,
           'following': following,
        }
        # print("Followers: %s\nFollowing: %s" %(followers, following))
        return render(request, self.template_name, context)


def edit_profile(request, user_id):
    profile_obj = Profile.objects.get(user_id = user_id)
    if request.user != profile_obj.user:
        return redirect('home')
    form= ProfileForm(instance = profile_obj)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id)

    context = {
        'form': form,
        'profile': profile_obj,
    }
    return render(request, 'edit_profile.html', context)
