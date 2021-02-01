from django import forms
from posts.models import Post, Comment, Reply, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'categories']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']
