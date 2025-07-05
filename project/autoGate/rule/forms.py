from django import forms
from tag.models import TagPermission


class TagPermissionFrom(forms.ModelForm):
    class Meta:
        model = TagPermission
        fields = ['permission_name', 'antenna', 'is_active']
        widgets = {
            'permission_name': forms.TextInput(attrs={'class': 'form-control'}),
            'antenna': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
