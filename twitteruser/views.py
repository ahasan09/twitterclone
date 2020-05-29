from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . import forms


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
