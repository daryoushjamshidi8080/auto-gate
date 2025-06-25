from django import forms
from . models import Tag, TagPermission


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['uid', 'owner_name', 'rule', 'is_active']
        widgets = {
            'uid': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rule': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uid'].widget.attrs['readonly'] = True
