from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'نام کاربری'}),
            "password": forms.TextInput(attrs={"type": "password", 'class' : 'form-control', 'placeholder' : 'رمز'})
        }