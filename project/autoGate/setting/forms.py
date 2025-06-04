from django import forms
from .models import antennas


class AntennaForm(forms.ModelForm):
    class Meta:
        model = antennas
        fields = ['number', 'name', 'open_time', 'is_active']
