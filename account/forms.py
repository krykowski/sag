#-*- coding: utf-8 -*-

from django import forms
from base.forms import ModelFormExt, FormExt
from django.contrib.auth.models import User

class UserCreateForm(ModelFormExt):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
    username = forms.CharField(label='Nazwa użytkownika')
    email = forms.CharField(label='E-mail')
    password = forms.CharField(label=u'Hasło', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label=u'Potwierdź hasło', widget=forms.PasswordInput())
    
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirmed = self.cleaned_data['confirm_password']
        
        if password != confirmed:
            raise forms.ValidationError("Hasła nie pasują do siebie")
    
class UserLoginForm(FormExt):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'span2', 'placeholder': u'Użytkownik'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'span2', 'placeholder': u'Hasło'}))
    
class UserUpdateForm(UserCreateForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    password = forms.CharField(label=u'Hasło', widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(label=u'Potwierdź hasło', widget=forms.PasswordInput(), required=False)
    
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirmed = self.cleaned_data['confirm_password']
        
        if password != confirmed:
            raise forms.ValidationError("Hasła nie pasują do siebie")
    