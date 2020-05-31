from django.db import models
from django.conf import settings
from tweet.models import Tweet
# Create your models here.


User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    related = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='related')
    read = models.BooleanField(default=False)
