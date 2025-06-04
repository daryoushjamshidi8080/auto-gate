from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'نام کاربری'}))
    password = forms.CharField(widget=forms.TextInput(attrs={"type": "password", 'class' : 'form-control', 'placeholder' : 'رمز'}))