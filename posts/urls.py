from django.urls import path
from . import views
from .views import PostListView, PostCreateView, PostUpdateView, PostDetailView, LikeView, FollowView

urlpatterns = [
	path('', views.index, name='index'),
	path('posts/', PostListView.as_view(), name='posts'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<str:slug>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<str:slug>/', PostDetailView.as_view(), name='post-detail'),
	path('post/<str:slug>/comment/', views.comment, name='comment'),
	path('post/<str:slug1>/<str:slug2>/reply/', views.replytocomment, name='replytocomment'),
	path('post/<str:username>/follow/', views.follow, name='follow'),
	path('post/<str:username>/unfollow/', views.unfollow, name='unfollow'),
	path('page-not-found/', views.error404, name='404'),
	path('form/', views.Form, name='form'),
	path('upload/', views.Upload, name='upload'),
	path('search/', views.search, name='search'),
	path('like/<int:pk>/', LikeView.as_view()),
	path('follow/<int:pk>/', FollowView.as_view()),
	path('add/category/', views.addCategory, name='add_category'),
	path('apiPosts/', views.apiPosts)
]