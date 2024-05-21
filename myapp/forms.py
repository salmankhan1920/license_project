# license_manager/forms.py
from django import forms
from .models import LicenseKey

class LicenseKeyForm(forms.ModelForm):
    class Meta:
        model = LicenseKey
        fields = ['key']


