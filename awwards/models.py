from django.db import models
from django.contrib.auth.models import User
import datetime as date
from django.urls import reverse


# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=255)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects", null=True, blank=True)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    design= models.IntegerField(default=0)
    usability= models.IntegerField(default=0)
    content = models.IntegerField(default=0)
    creativity = models.IntegerField(default=0)

    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)

