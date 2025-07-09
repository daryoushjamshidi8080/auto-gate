from django import forms
from . models import Tag, TagPermission


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['uid', 'tag_number', 'owner_name', 'rule', 'is_active',
                  'car_name', 'pelicula', 'number_unit', 'tag_number']
        widgets = {
            'uid': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'car_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pelicula': forms.TextInput(attrs={'class': 'form-control'}),
            'number_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'rule': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uid'].widget.attrs['readonly'] = True
        # self.fields['tag_number'].widget.attrs['readonly'] = True


class SearchTagForm(forms.Form):
    search_tag = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_tag'].widget.attrs['placeholder'] = 'جستجو'


class SearchTagAnonymousForm(forms.Form):
    search_tag_anonymous = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_tag_anonymous'].widget.attrs['placeholder'] = 'جستجو'
