from django.db import models
from django.utils import timezone, dateformat
from django.contrib.auth.models import User
import random


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.CharField(max_length=200)

    def setProfile(self):
        self.profile_img = f"https://avatars.dicebear.com/api/identicon/:{self.user.username}.svg"


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=35)
    description = models.CharField(max_length=100)
    body = models.CharField(max_length=500)
    date_posted = models.DateTimeField(
        default=dateformat.format(timezone.now(), 'Y-m-d H:i:s'))
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
