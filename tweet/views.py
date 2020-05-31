from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from twitteruser.models import TwitterUser
from tweet.models import Tweet
from notification.models import Notification
from tweet.forms import TweetForm
from django.contrib.auth.decorators import login_required
from twitteruser.models import FollowModel
from django.conf import settings
from django.db.models import Q

# User = settings.AUTH_USER_MODEL

# Create your views here.
@login_required
def home(request):
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
        unread_notifications = Notification.objects.filter(
            receiver=user, read=False)
        unread_count = unread_notifications.count()
        tweets = Tweet.objects.filter(
            Q(user__followed__follower=user.id) | Q(user=user)).order_by('-creation_date')
        tweet_count = Tweet.objects.filter(user=user).count()

    except ObjectDoesNotExist:
        tweets = None
        tweet_count = 0

    return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'clickable': clickable, 'user': user, 'follow': follow,
                                         'followings_count': followings_count, 'followers_count': followers_count, 'unread_count': unread_count})


def tweet(request, id=''):
    tweet_count = 0
    followings_count = 0
    followers_count = 0
    clickable = True
    follow = False
    unread_count = 0

    if request.user.is_authenticated:
        followings = FollowModel.objects.filter(follower=request.user)
        followers = FollowModel.objects.filter(followed=request.user)
        followings_count = followings.count()
        followers_count = followers.count()

        try:
            unread_notifications = Notification.objects.filter(
                receiver=request.user, read=False)
            unread_count = unread_notifications.count()
            current_user_tweets = Tweet.objects.filter(
                Q(user__followed__follower=request.user.id) | Q(user=request.user)).order_by('-creation_date')
            tweet_count = Tweet.objects.filter(user=request.user).count()

            if id:
                tweets = Tweet.objects.filter(pk=id)
                clickable = False
            else:
                tweets = current_user_tweets
        except ObjectDoesNotExist:
            tweets = None
            tweet_count = 0

        return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'clickable': clickable, 'user': request.user, 'follow': follow,
                                             'followings_count': followings_count, 'followers_count': followers_count,
                                             'unread_count': unread_count})
    else:
        tweets = Tweet.objects.filter(pk=id)
        return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'clickable': clickable, 'user': None, 'follow': follow,
                                             'followings_count': followings_count, 'followers_count': followers_count,
                                             'unread_count': unread_count})


def selected_user(request, username=''):
    tweet_count = 0
    clickable = True
    user = None
    follow = True
    unread_count = 0

    current_user = get_object_or_404(TwitterUser, pk=request.user.id)

    if username:
        clickable = False
        user = get_object_or_404(TwitterUser, username=username)
        if user.id == request.user.id:
            follow = False
        elif FollowModel.objects.filter(follower=current_user,
                                        followed=user) .exists():
            follow = False
        else:
            follow = True
    else:
        user = current_user
        follow = False

    followings = FollowModel.objects.filter(follower=user)
    followers = FollowModel.objects.filter(followed=user)
    followings_count = followings.count()
    followers_count = followers.count()

    try:
        unread_notifications = Notification.objects.filter(
            receiver=user, read=False)
        unread_count = unread_notifications.count()
        tweets = Tweet.objects.filter(
            Q(user__followed__follower=user.id) | Q(user=user)).order_by('-creation_date')
        tweet_count = Tweet.objects.filter(user=user).count()
    except ObjectDoesNotExist:
        tweets = None
        tweet_count = 0

    return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'clickable': clickable, 'user': user, 'follow': follow,
                                         'followings_count': followings_count, 'followers_count': followers_count,
                                         'unread_count': unread_count})


@login_required
def compose(request):
    tweet_count = 0
    user = None
    follow = False
    unread_count = 0

    user = get_object_or_404(TwitterUser, pk=request.user.id)

    followings = FollowModel.objects.filter(follower=user)
    followers = FollowModel.objects.filter(followed=user)
    followings_count = followings.count()
    followers_count = followers.count()

    try:
        unread_notifications = Notification.objects.filter(
            receiver=user, read=False)
        unread_count = unread_notifications.count()
        tweet_count = Tweet.objects.filter(user=user).count()

    except ObjectDoesNotExist:
        tweet_count = 0

    form = TweetForm()
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            mentions = tweet.parse_mentions()
            print(mentions)
            if mentions:
                for mention in mentions:
                    notification_instance = Notification(
                        sender=request.user, receiver=mention,
                        related=tweet)
                    notification_instance.save()
            return redirect('home')
    return render(request, 'compose.html', {'form': form, 'tweet_count': tweet_count, 'user': user, 'follow': follow, 'followings_count': followings_count, 'followers_count': followers_count, 'unread_count': unread_count})
