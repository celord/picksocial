from django.forms import ModelForm
from django import forms
from .models import Post, Reply, Comment


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        labels = {
            'body': 'Caption',
            'tags': 'Category'
        }
        widgets = {
            'url': forms.TextInput(attrs={'placeholder': 'Enter the URL of the image...'}),
            'body': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Write your caption here...', 'class': 'font1 text-4xl'}),
            'tags': forms.CheckboxSelectMultiple()
        }


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tags']
        labels = {
            'body': '',
            'tags': 'Category'
        }
        widgets = {
            'body': forms.Textarea(
                attrs={'rows': 3, 'class': 'font1 text-4xl'}),
            'tags': forms.CheckboxSelectMultiple()
        }

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            'body': forms.TextInput(
                attrs={'placeholder': 'Add comment...',  'type': 'text', 'name': 'comment', 'max_length': '150'}),
        }

class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            'body': forms.TextInput(
                attrs={'placeholder': 'Add reply...',  'class': '!text-sm'}),
        }