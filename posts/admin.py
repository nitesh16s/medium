from django.contrib import admin
from .models import Post, Comment, Reply, Like, PostComment

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)
admin.site.register(PostComment)
