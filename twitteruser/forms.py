from django import forms
from twitteruser.models import TwitterUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpForm(forms.ModelForm):
    class Meta:
        model = TwitterUser
        fields = ['username', 'first_name',
                  'last_name', 'password', 'email', 'phone', ]
