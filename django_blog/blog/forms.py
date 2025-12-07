# django_blog/blog/forms.py
from django import forms
from django.forms import ModelForm
from .models import Post
from .models import Profile

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # author set in the view
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Write your content...'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')
