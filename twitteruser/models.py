from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class TwitterUser (AbstractUser):
    phone = models.CharField(null=True, max_length=15)
