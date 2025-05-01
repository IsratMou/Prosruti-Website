from django import forms
from django.utils import timezone
from .models import Session, SessionNote, Counselor, Resource, SharedResource


class CounselorForm(forms.ModelForm):
    """Form for creating and updating counselor profiles"""

    class Meta:
        model = Counselor
        fields = ['bio', 'specialization', 'qualification', 'experience', 'is_available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SessionForm(forms.ModelForm):
    """Form for creating and updating counseling sessions"""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SessionForm, self).__init__(*args, **kwargs)

        # If form is used by a counselor, they may see all clients
        if self.user and hasattr(self.user, 'counselor_profile'):
            self.fields['client'].queryset = self.fields['client'].queryset.all()
        else:
            # If user is a client, they can only book sessions for themselves
            self.fields.pop('client')

    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Session
        fields = ['counselor', 'client', 'title', 'description', 'session_type',
                  'scheduled_at', 'duration', 'meeting_link']
        widgets = {
            'counselor': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'session_type': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
        }