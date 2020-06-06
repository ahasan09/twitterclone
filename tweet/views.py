from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from twitteruser.models import TwitterUser
from tweet.models import Tweet
from notification.models import Notification
from tweet.forms import TweetForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    tweet_count = 0
    unread_count = 0
    user = request.user
    followers = user.followers.all()
    followers_count = followers.count()

    try:
        unread_notifications = Notification.objects.filter(
            receiver=user, read=False)
        unread_count = unread_notifications.count()
        my_tweets = Tweet.objects.filter(user=user)
        tweets = list(my_tweets)
        for follower in followers:
            for post in Tweet.objects.filter(user=follower):
                tweets.append(post)
        tweets.sort(key=lambda r: r.creation_date, reverse=True)
        tweet_count = my_tweets.count()

    except ObjectDoesNotExist:
        tweets = None
        tweet_count = 0

    return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'user': user, 'followers_count': followers_count, 'unread_count': unread_count})


def tweet(request, id=''):
    tweet_count = 0
    followers_count = 0
    follow = False
    unread_count = 0

    if request.user.is_authenticated:
        user = request.user
        followers = user.followers.all()
        followers_count = followers.count()

        try:
            unread_notifications = Notification.objects.filter(
                receiver=user, read=False)
            unread_count = unread_notifications.count()
            my_tweets = Tweet.objects.filter(user=user)
            tweets = list(my_tweets)
            for follower in followers:
                for post in Tweet.objects.filter(user=follower):
                    tweets.append(post)
            tweets.sort(key=lambda r: r.creation_date, reverse=True)
            tweet_count = my_tweets.count()
            if id:
                tweets = Tweet.objects.filter(pk=id)

        except ObjectDoesNotExist:
            tweets = None
            tweet_count = 0
    else:
        tweet = get_object_or_404(Tweet, id=id)
        user = None
        tweets = []
        tweets.append(tweet)

    return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'user': user, 'follow': follow, 'followers_count': followers_count, 'unread_count': unread_count})


def selected_user(request, username=''):
    tweet_count = 0
    unread_count = 0
    is_follow = False
    user = get_object_or_404(TwitterUser, username=username)
    followers = user.followers.all()
    followers_count = followers.count()

    if request.user.is_authenticated:
        myfollowers = request.user.followers.all()
        if user in myfollowers:
            is_follow = True
        else:
            is_follow = False

    try:
        unread_notifications = Notification.objects.filter(
            receiver=user, read=False)
        unread_count = unread_notifications.count()
        my_tweets = Tweet.objects.filter(user=user)
        tweets = list(my_tweets)
        for follower in followers:
            for post in Tweet.objects.filter(user=follower):
                tweets.append(post)
        tweets.sort(key=lambda r: r.creation_date, reverse=True)
        tweet_count = my_tweets.count()
    except ObjectDoesNotExist:
        tweets = None
        tweet_count = 0

    return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'user': user, 'is_follow': is_follow, 'followers_count': followers_count, 'unread_count': unread_count})


@login_required
def compose(request):
    tweet_count = 0
    unread_count = 0
    user = request.user
    followers = user.followers.all()
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
    return render(request, 'compose.html', {'form': form, 'tweet_count': tweet_count, 'user': user, 'followers_count': followers_count, 'unread_count': unread_count})
