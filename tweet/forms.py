from django import forms
from tweet.models import Tweet


class TweetForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Tweet
        fields = ('body',)
