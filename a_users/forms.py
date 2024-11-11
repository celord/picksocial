from .models import *
from django.forms import ModelForm
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'created']
        labels = {
            'realname': 'Real Name',
        }

        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }