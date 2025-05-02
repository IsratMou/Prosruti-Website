from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    """Form for making donations"""
    class Meta:
        model = Donation
        fields = [
            'amount', 'payment_method', 'donor_name',
            'donor_email', 'donor_phone', 'message', 'is_anonymous'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '10'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'donor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'donor_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'donor_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
