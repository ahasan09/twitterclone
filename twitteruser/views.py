from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . import forms
from twitteruser.models import (FollowModel, TwitterUser)
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def signup(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('/')
    else:
        form = forms.SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_action(request):
    logout(request)
    return redirect(request.GET.get("next", reverse('login')))


# User = settings.AUTH_USER_MODEL


@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            current_user = get_object_or_404(TwitterUser, pk=request.user.id)
            other_user = get_object_or_404(TwitterUser, pk=follow_id)
            if FollowModel.objects.filter(follower=current_user,
                                          followed=other_user) .exists():
                pass  # Do not save a model if it already exists.
            else:
                follow_instance = FollowModel(
                    follower=current_user, followed=other_user)
                follow_instance.save()
    return redirect('/'+other_user.username+'/')


@login_required
def unfollow(request):
    if request.method == "POST":
        follow_id = request.POST.get('unfollow', False)
        if follow_id:
            current_user = get_object_or_404(TwitterUser, pk=request.user.id)
            other_user = get_object_or_404(TwitterUser, pk=follow_id)
            FollowModel.objects.get(follower=current_user,
                                    followed=other_user).delete()
        else:
            pass
    return redirect('/'+other_user.username+'/')
