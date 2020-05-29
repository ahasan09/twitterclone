from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from twitteruser.models import TwitterUser
from tweet.models import Tweet
from tweet.forms import TweetForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request, id='', username=''):
    tweet_count = 0
    clickable = True
    user = None

    if username:
        clickable = False
        user = get_object_or_404(TwitterUser, username=username)
    else:
        user = get_object_or_404(TwitterUser, pk=request.user.id)

    try:
        if id:
            tweets = Tweet.objects.filter(pk=id)
            tweet_count = Tweet.objects.filter(
                user=user).order_by('-creation_date').count()
            clickable = False
        else:
            # tweets = Tweet.objects.filter(
            #     user=user).order_by('-creation_date')
            tweets = Tweet.objects.all().order_by('-creation_date')
            tweet_count = tweets.count()
    except ObjectDoesNotExist:
        tweets = None
        tweet_count = 0
    return render(request, 'home.html', {'tweets': tweets, 'tweet_count': tweet_count, 'clickable': clickable, 'user': user})


@login_required
def compose(request):
    form = TweetForm()
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('home')
    return render(request, 'compose.html', {'form': form})
