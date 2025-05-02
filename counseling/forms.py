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

    def clean_scheduled_at(self):
        scheduled_at = self.cleaned_data.get('scheduled_at')
        if scheduled_at and scheduled_at < timezone.now():
            raise forms.ValidationError("Session cannot be scheduled in the past")
        return scheduled_at


class SessionUpdateForm(forms.ModelForm):
    """Form for updating session status"""

    class Meta:
        model = Session
        fields = ['status', 'meeting_link']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
        }


class SessionNoteForm(forms.ModelForm):
    """Form for creating and updating session notes"""

    class Meta:
        model = SessionNote
        fields = ['note', 'is_private']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ResourceForm(forms.ModelForm):
    """Form for creating and updating resources"""

    class Meta:
        model = Resource
        fields = ['title', 'description', 'resource_type', 'url', 'file', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SharedResourceForm(forms.ModelForm):
    """Form for sharing resources with clients"""

    class Meta:
        model = SharedResource
        fields = ['resource', 'client', 'session', 'note']
        widgets = {
            'resource': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'session': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.counselor = kwargs.pop('counselor', None)
        super(SharedResourceForm, self).__init__(*args, **kwargs)

        if self.counselor:
            # Filter resources created by this counselor
            self.fields['resource'].queryset = Resource.objects.filter(
                created_by=self.counselor
            ) | Resource.objects.filter(is_public=True)

            # Filter sessions conducted by this counselor
            self.fields['session'].queryset = Session.objects.filter(
                counselor=self.counselor
            )

            # Filter clients who have had sessions with this counselor
            self.fields['client'].queryset = self.fields['client'].queryset.filter(
                counseling_sessions__counselor=self.counselor
            ).distinct()