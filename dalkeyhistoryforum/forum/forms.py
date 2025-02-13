from django import forms
from .models import Thread, Post

class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('title', 'topic')

class FirstPostCreateForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['content', 'image']

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['content', 'image']