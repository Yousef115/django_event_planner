from django.urls import path
from .views import ( Login, Logout, Signup, Home, dashboard, create_event, 
	EventDetail, edit_event, follow)

urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('<int:event_id>', Home.as_view(), name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('dashboard/', dashboard , name='dashboard'),

    path('event/create/', create_event , name='create-event'),
    path('event/<int:event_id>/edit/', edit_event , name='edit-event'),
    path('event/<int:event_id>/detail/', EventDetail.as_view() , name='detail-event'),

    path('profile/<int:user_id>/follow/', follow , name='follow'),

]


