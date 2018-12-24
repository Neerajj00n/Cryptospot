from django import forms
from .models import *

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="plz enter")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'views', 'category']