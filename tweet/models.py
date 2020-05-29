from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.


User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    body = models.CharField(max_length=140)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-creation_date",)

    def __str__(self):
        return self.body
