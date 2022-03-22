from django import forms
from .models import Feed, Comment

class FeedForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '2',
            'placeholder': 'Say Something...'
        }))

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
            })
    )

    class Meta:
        model = Feed
        fields = ['body']