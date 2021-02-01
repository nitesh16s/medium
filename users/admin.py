from django.contrib import admin
from .models import Profile, Connections, SavePost

admin.site.register(Profile)
admin.site.register(Connections)
admin.site.register(SavePost)