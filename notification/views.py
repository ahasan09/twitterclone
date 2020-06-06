from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from tweet.models import Tweet
from notification.models import Notification
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def notification(request):
    tweet_count = 0
    unread_count = 0
    user = request.user
    followers = user.followers.all()
    followers_count = followers.count()

    try:
        tweets = []
        notifications = Notification.objects.filter(
            receiver=user, read=False)
        for item in notifications:
            tweets.append(item.related)
        tweets.sort(key=lambda r: r.creation_date, reverse=True)
        Notification.objects.filter(
            receiver=user, read=False).update(read=True)
        tweet_count = Tweet.objects.filter(user=user).count()

    except ObjectDoesNotExist:
        tweets = None
        tweet_count = 0

    return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'user': user, 'followers_count': followers_count, 'unread_count': unread_count, 'is_notification': True})
