from django.urls import path
from .views import get_all_loggedIn_users


urlpatterns = [
    path('loggedIn-users/', get_all_loggedIn_users, name='loggedInUsers')
]