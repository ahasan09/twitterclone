from django.db import models
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify
from twitteruser.models import TwitterUser
# Create your models here.


User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    body = models.CharField(max_length=140)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-creation_date",)

    def __str__(self):
        return self.body

    def parse_mentions(self):
        mentions = [slugify(i) for i in self.body.split() if i.startswith("@")]
        print(mentions)
        return TwitterUser.objects.filter(username__in=mentions)

    def parse_all(self):
        parts = self.body.split()
        mention_counter = 0
        result = {"parsed_text": "", "mentions": []}
        for index, value in enumerate(parts):
            if value.startswith("@"):
                parts[index] = "{mention" + str(mention_counter) + "}"
                mention_counter += 1
                result[u'mentions'].append(slugify(value))
        result[u'parsed_text'] = " ".join(parts)
        return result
