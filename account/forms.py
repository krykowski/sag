from django import forms
from base.forms import ModelFormExt
from django.contrib.auth.models import User

class UserCreateForm(ModelFormExt):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }
        
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())