from django.urls import path
from . import views
from .views import ProfileCreateView, ProfileUpdateView, SavePostView, UserPostListView, UnFollowView

urlpatterns = [
	path('accounts/<str:username>/posts/', UserPostListView.as_view(), name='user-posts'),
	path('accounts/<str:username>/profile/', views.profile, name='profile'),
	path('accounts/profile/create/', ProfileCreateView.as_view(), name='create-profile'),
	path('accounts/profile/<str:slug>/update/', ProfileUpdateView.as_view(), name='update-profile'),
	path('save/<int:pk>/', SavePostView.as_view(), name='save-post'),
	path('accounts/profile/<str:username>/followers/', views.followers, name='followers'),
	path('accounts/profile/<str:username>/followings/', views.followings, name='followings'),
	path('accounts/<str:username>/savedposts/', views.savedPosts, name='savedPosts'),
	path('unfollow/<int:pk>/', UnFollowView.as_view()),
]