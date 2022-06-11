from django.db import models
from django.contrib.auth.models import User
import datetime as date

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', default='default.png')
    username = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=60, blank=True)
    contact = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return self.username


class Project(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(max_length=255, default='https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?f=y')
    link = models.URLField(max_length=255)
    profile = models.ManyToManyField(Profile)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

