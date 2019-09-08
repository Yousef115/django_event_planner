from django.urls import path
from .views import Login, Logout, Signup, home, dashboard, create_event, event_detail, edit_event

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('dashboard/', dashboard , name='dashboard'),
    path('event/<int:event_id>/detail/', event_detail , name='detail-event'),
    path('event/<int:event_id>/edit/', edit_event , name='edit-event'),
    path('event/create/', create_event , name='create-event'),
]