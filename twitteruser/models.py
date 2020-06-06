from django.db import models
from django.contrib.auth.models import AbstractUser


class TwitterUser (AbstractUser):
    phone = models.CharField(null=True, max_length=15)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)
