from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='static/profile/')
    website_url = models.URLField(max_length=255, blank=True, null=True)
    weibo_url = models.URLField(max_length=255, blank=True, null=True)
    twitter_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(blank=True, null=True, upload_to='article/%Y%m%d/')
    snippet = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(default=timezone.now)
    modified_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def total_like(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=(str(self.id)))

    def save(self, *args, **kwargs):
        self.modified_date = timezone.now()
        super().save(*args, **kwargs)
