from django import forms


class LogsForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs['placeholder'] = 'جستجو'
