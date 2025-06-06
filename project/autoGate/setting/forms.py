from django import forms
from .models import antennas
from django.contrib.auth.models import User



class AntennaForm(forms.ModelForm):
    class Meta:
        model = antennas
        fields = ['number', 'name', 'open_time', 'is_active']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'open_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CusstomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_staff  = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})) 
    is_superuser = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:   
        model = User
        fields = ['username', 'password', 'is_staff', 'is_superuser', 'first_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        print(password, password2)
        if password and password2 and password != password2:
            raise forms.ValidationError("رمز عبور و تکرار آن یکسان نیستند.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit :
            user.save()
        return user
