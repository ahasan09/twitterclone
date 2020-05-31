from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from twitteruser.models import TwitterUser
from tweet.models import Tweet
from notification.models import Notification
from django.contrib.auth.decorators import login_required
from twitteruser.models import FollowModel

# Create your views here.
@login_required
def notification(request):
    tweet_count = 0
    clickable = True
    user = None
    follow = False
    unread_count = 0

    user = get_object_or_404(TwitterUser, pk=request.user.id)

    followings = FollowModel.objects.filter(follower=user)
    followers = FollowModel.objects.filter(followed=user)
    followings_count = followings.count()
    followers_count = followers.count()

    try:
        tweets = []
        notifications = Notification.objects.filter(
            receiver=user, read=False)
        for item in notifications:
            tweets.append(item.related)
        print(tweets)
        Notification.objects.filter(
            receiver=user, read=False).update(read=True)
        tweet_count = Tweet.objects.filter(user=user).count()

    except ObjectDoesNotExist:
        tweets = None
        tweet_count = 0

    return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'clickable': clickable, 'user': user, 'follow': follow,
                                         'followings_count': followings_count, 'followers_count': followers_count,
                                         'unread_count': unread_count,
                                         'is_notification': True})
