from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from . import forms
from twitteruser.models import TwitterUser


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


@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            user = request.user
            follow = TwitterUser.objects.get(id=follow_id)
            user.followers.add(follow)
            user.save()
        else:
            pass
    return redirect('/'+follow.username+'/')


@login_required
def unfollow(request):
    if request.method == "POST":
        follow_id = request.POST.get('unfollow', False)
        if follow_id:
            user = request.user
            follow = TwitterUser.objects.get(id=follow_id)
            user.followers.remove(follow)
            user.save()
        else:
            pass
    return redirect('/'+follow.username+'/')
