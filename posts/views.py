from django.contrib.auth import models
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from .models import Category, Post, Comment, Reply, Like
from .forms import PostForm, CommentForm, ReplyForm, CategoryForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from users.models import Connections, SavePost


@login_required
def index(request):
    posts = Post.objects.select_related(
        'author__profile').filter().order_by('-created')
    saved = SavePost.objects.filter(author=request.user)
    savedPostsIds = []
    for post in saved:
        savedPostsIds.append(post.post_id)
    return render(request, 'main/index.html', {'posts': posts, 'savedPosts': savedPostsIds})


def apiPosts(request):
    return render(request, 'main/apiPosts.html')


class PostListView(LoginRequiredMixin, ListView):
    '''
    List all posts of users which are followed by request user.
    '''
    model = Post
    template_name = 'posts/posts.html'

    def get_followings(self):
        followings = Connections.objects.filter(
            follower_id=self.request.user.id).values_list('following_id')
        return followings

    def get_following_posts(self):
        followings = self.get_followings()
        posts = Post.objects.select_related(
            'author__profile').filter(author__in=followings)
        return posts

    def get_saved_posts(self):
        saved = SavePost.objects.filter(
            author=self.request.user).values_list('post_id')
        return saved

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['following_posts'] = self.get_following_posts()
        context_data['saved_posts'] = self.get_saved_posts()
        return context_data


class PostCreateView(LoginRequiredMixin, CreateView):

    def get(self, request, *args, **kwargs):
        context = {
            'category_form': CategoryForm(),
            'post_form': PostForm()
        }
        return render(request, 'posts/post_form.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')
            categories = request.POST.getlist('categories')
            try:
                image = request.FILES.get('image')
            except:
                image = None
            post = Post(author=request.user, title=title,
                        content=content, image=image)
            post.save()
            for category in categories:
                post.categories.add(category)
            messages.success(request, 'Post added successfully.')
            return redirect('post-detail', slug=post.slug)
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('post-create')


class PostDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.select_related(
                'author__profile').get(slug=kwargs['slug'])
        except Post.DoesNotExist:
            return redirect('404')

        saved = SavePost.objects.filter(author=self.request.user)
        savedPostsIds = []
        for s in saved:
            savedPostsIds.append(s.post_id)

        if Connections.objects.filter(follower__username=self.request.user, following=post.author).exists():
            follows = True
        else:
            follows = False

        if Like.objects.filter(user=self.request.user, post=post).exists():
            like = True
        else:
            like = False

        likes_count = Like.objects.filter(post=post).count()

        comments_count = Comment.objects.filter(post=post).count()

        context = {'post': post, 'follows': follows, 'like': like, 'likes_count': likes_count,
                   'comments_count': comments_count, 'savedPosts': savedPostsIds}

        return render(request, 'posts/post_detail.html', context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'content', 'categories']
    template_name = 'posts/update_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def addCategory(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        category = request.POST.get('category')
        category = Category(category=category)
        try:
            category.save()
        except:
            messages.warning(request, 'Category already present.')
        return redirect('post-create')
    else:
        return redirect('404')


@login_required
def comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment = request.POST.get('content')
            comment = Comment.objects.create(
                post=post, author=request.user, content=comment)
            comment.save()
            return redirect('/post/{}/comment/'.format(post.slug))

    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'posts/comments.html', context)


@login_required
def replytocomment(request, slug1, slug2):
    post = get_object_or_404(Post, slug=slug1)
    comment = get_object_or_404(Comment, slug=slug2)
    replies = Reply.objects.filter(comment=comment).order_by('-id')

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST or None)
        if reply_form.is_valid():
            reply = request.POST.get('content')
            reply = Reply.objects.create(
                comment=comment, author=request.user, content=reply)
            reply.save()
            return redirect('/post/{}/{}/reply/'.format(post.slug, comment.slug))

    else:
        reply_form = ReplyForm()

    context = {
        'post': post,
        'comment': comment,
        'replies': replies,
        'reply_form': reply_form,
    }

    return render(request, 'posts/replies.html', context)


@login_required
def follow(request, *args, **kwargs):
    follower = User.objects.get(username=request.user)
    following = User.objects.get(username=kwargs['username'])

    if follower == following:
        messages.warning(request, 'You cannot follow yourself.')

    else:
        connection = Connections.objects.get_or_create(
            follower=follower, following=following)

        if connection:
            messages.success(
                request, 'You\'ve successfully followed {}.'.format(following.username))
        else:
            messages.warning(
                request, 'You\'ve already followed {}.'.format(following.username))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow(request, *args, **kwargs):
    follower = User.objects.get(username=request.user)
    following = User.objects.get(username=kwargs['username'])

    if follower == following:
        messages.warning(request, 'You cannot follow yourself.')

    else:
        connection = Connections.objects.get(
            follower=follower, following=following)

        connection.delete()

        messages.success(
            request, 'You\'ve unfollwed {}.'.format(following.username))

    return redirect(request.META.get('HTTP_REFERER'))


class FollowView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, pk=None, *args, **kwargs):

        follower = User.objects.get(username=request.user)
        post = Post.objects.get(id=pk)
        following = post.author

        if follower == following:
            return Response('Fuck You')

        connection = Connections.objects.filter(
            follower=follower, following=following).exists()

        if connection is False:
            connection = Connections.objects.create(
                follower=follower, following=following)
            connected = True
            img = "<a title='Unfollow'>Unfollow</a>"

        else:
            connection = Connections.objects.get(
                follower=follower, following=following)
            connection.delete()
            connected = False
            img = "<a title='Follow'>Follow</a>"

        data = {
            'connected': connected,
            'img': img,
        }

        # connected is not getting used in frontend

        return Response(data)


class LikeView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, *args, **kwargs):
        post = Post.objects.get(id=pk)
        user = self.request.user
        like = Like.objects.filter(user=request.user, post=post).exists()

        if like is False:
            like = Like.objects.create(post=post, user=request.user)
            liked = True
            img = "<i title='Dislike' class='fa fa-heart' style='font-size: 20px;'>"
            likes_count = Like.objects.filter(post=post).count()
        else:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            liked = False
            img = "<i title='Like' class='fa fa-heart-o' style='font-size: 20px;'>"
            likes_count = Like.objects.filter(post=post).count()

        data = {
            'liked': liked,
            'img': img,
            'likes_count': likes_count,
        }

        return Response(data)


# @login_required
# def like(request, *args, **kwargs):
#     post = Post.objects.get(slug=kwargs['slug'])
#     like = Like.objects.get_or_create(post=post, user=request.user)

#     if like:
#         messages.success(request, 'You\'ve liked the post.')
#         return HttpResponseRedirect(reverse('post-detail', kwargs= {'slug':post.slug}))


# @login_required
# def dislike(request, *args, **kwargs):
#     like = Like.objects.get(post__slug=kwargs['slug'])
#     like.delete()

#     messages.success(request, 'You\'ve disliked the post.')

#     return redirect(request.META.get('HTTP_REFERER'))


def error404(request):
    return render(request, 'main/404.html')


def Form(request):
    return render(request, "posts/uploads.html", {})


def Upload(request):
    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            with open('/home/nitesh2/Codes/Projects/Django/myProjects/blogs/media/files/' + str(count), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        process(x)
    return HttpResponse("File(s) uploaded!")


def search(request):
    query = request.GET.get('q')

    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(tags__icontains=query)
    )
    return render(request, 'posts/search.html', {'results': results})
