from django import forms
from django.db import models
from django.conf import settings
from .views import authenticate
from django.core.validators import RegexValidator
from .models import Post

User = settings.AUTH_USER_MODEL


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(label="Title", required=True, max_length=100)
    # title_image = forms.ImageField(required=False)
    content = forms.CharField( widget=forms.Textarea, label="Content", required=True)
    class Meta:
        model = Post
        fields = (
            'title',
            'title_image',
            'content'
        )

class UpdateForm(forms.ModelForm):
    title = forms.CharField(label="Title", required=True, max_length=100
                            , widget=forms.TextInput(attrs={'placeholder': 'title'}))
    content = forms.CharField( widget=forms.Textarea, label="Content", required=True)
    
    class Meta:
        model = Post
        fields = (
            'title',
            'title_image',
            'content'
        )