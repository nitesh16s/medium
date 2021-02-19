from django.http.response import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


def get_all_loggedIn_users(request):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        print(data)
        uid_list.append(data.get('_auth_user_id', None))
    
    print(uid_list)

    # Query all logged in users based on id list
    users = User.objects.filter(id__in=uid_list)
    return HttpResponse(users)