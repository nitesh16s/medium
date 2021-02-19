from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Profile, Connections, SavePost
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from posts.models import Post


class UserPostListView(ListView):
    template_name = 'users/user_posts.html'
    context_object_name = 'user_posts'

    def get_queryset(self):
        user_posts = Post.objects.select_related('author__profile').filter(
            author=self.request.user).order_by('-id')
        return user_posts

    # def get(self, request, *args, **kwargs):
    #     user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     posts = Post.objects.select_related(
    #         'author__profile').all().filter(author=user)
    #     return render(request, 'users/user_posts.html', {'posts': posts, 'user': user})


@login_required
def savedPosts(request, username):
    savedPosts = []
    ids = list(SavePost.objects.filter(
        author=request.user).order_by('-post_id'))
    for id in ids:
        savedPosts.append(Post.objects.get(id=str(id)))
    return render(request, 'users/savedPosts.html', {'savedPosts': savedPosts})


@login_required
def profile(request, username):
    followers = Connections.objects.all().filter(following=request.user)
    followings = Connections.objects.all().filter(follower=request.user)
    posts = Post.objects.all().filter(author=request.user).order_by('-created')
    return render(request, 'users/profile.html', {'posts': posts, 'followers': followers, 'followings': followings, 'followings_count': followings.count})


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['first_name', 'last_name', 'is_male',
              'is_female', 'about', 'image', 'background']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'is_male',
              'is_female', 'about', 'image', 'background']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class SavePostView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, *args, **kwargs):
        post = Post.objects.get(id=pk)
        user = self.request.user
        savedPosts = []
        ids = list(SavePost.objects.filter(author=request.user))
        for id in ids:
            savedPosts.append(Post.objects.get(id=str(id)))
        saved = False

        if post in savedPosts:
            savepost = SavePost.objects.get(post=post, author=user)
            savepost.delete()
            saved = False
            img = "<i title='Save Post' class='fa fa-bookmark-o' style='font-size: 20px;'>"
            p = '<p>SavePost</p>'
        else:
            SavePost.objects.create(post=post, author=user)
            saved = True
            img = "<i title='Unsave Post' class='fa fa-bookmark' style='font-size: 20px;'>"
            p = '<p>Unsave Post</p>'

        data = {
            'saved': saved,
            'img': img,
            'p': p
        }

        return Response(data)


def followers(request, username):
    followers = Connections.objects.all().filter(following=request.user)
    return render(request, 'users/followers.html', {'followers': followers})


def followings(request, username):
    followings = Connections.objects.all().filter(follower=request.user)
    return render(request, 'users/followings.html', {'followings': followings})


class UnFollowView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, pk=None, *args, **kwargs):

        following = User.objects.get(id=pk)
        follower = self.request.user

        connection = Connections.objects.get(
            follower=follower, following=following)

        connection.delete()

        followers_count = Connections.objects.all().filter(following=request.user).count()
        followings_count = Connections.objects.all().filter(follower=request.user).count()

        data = {
            'followers_count': followers_count,
            'followings_count': followings_count
        }
        return Response(data)
