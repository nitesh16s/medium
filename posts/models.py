from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from mptt.models import MPTTModel, TreeForeignKey

# CATEGORY_CHOICE = (
#     ('Art', 'Art'),
#     ('Buisness', 'Buisness'),
#     ('Cooking', 'Cooking'),
#     ('Design', 'Design'),
#     ('Education', 'Education'),
#     ('Engineering', 'Engineering'),
#     ('Entertainment', 'Entertainment'),
#     ('Food', 'Food'),
#     ('Goverment', 'Goverment'),
#     ('Healthcare', 'Healthcare'),
#     ('Languages', 'Languages'),
#     ('Law', 'Law'),
#     ('Mathematics', 'Mathematics'),
#     ('Politics', 'Politics'),
#     ('Science', 'Science'),
#     ('Sports', 'Sports'),
#     ('Technology', 'Technology'),
#     ('Traveling', 'Traveling'),
# )


class Category(models.Model):
    category = models.CharField(
        help_text='Create new category', max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.category))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.category)


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_user')
    title = models.CharField(('Title...'), max_length=200)
    image = models.ImageField(
        ('Background Image...'), blank=True, default='default.jpg', upload_to='post_images')
    content = RichTextUploadingField(help_text='Use responsive images')
    categories = models.ManyToManyField(
        Category, help_text='Select related categories...')
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('index')

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title[0: 50]))
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        (x, y) = img.size
        new_x = 768
        new_y = int(new_x * (y / x))
        output_size = (new_x, new_y)
        img.thumbnail(output_size)
        img.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(('Comment goes here...'))
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=50, default='None')

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.content))
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.slug])


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(('Reply goes here...'))
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs=[self.slug, self.id])

    def __str__(self):
        return self.content


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} liked by {}'.format(self.post, self.user)


class PostComment(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
