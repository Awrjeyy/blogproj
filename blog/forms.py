from django import forms
from .views import authenticate
from django.core.validators import RegexValidator
from .models import Post


STATUS_CHOICES = [
    (1, 'Publish'),
    (2, 'Draft'),
]
class CreatePostForm(forms.ModelForm):
    title = forms.CharField(label="Title", required=True, max_length=100)
    content = forms.TextField(label="Content", required=True)
    status = forms.MultipleChoiceField(required=True, 
                                        widget=forms.CheckboxSelectMultiple,
                                        choices=STATUS_CHOICES,
    )
    class Meta:
        model = Post
        fields = (
            'title',
            'content'
        )