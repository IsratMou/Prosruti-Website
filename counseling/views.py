from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q

from .models import Session, SessionNote, Counselor, Resource, SharedResource
from .forms import (
    SessionForm, SessionUpdateForm, SessionNoteForm,
    CounselorForm, ResourceForm, SharedResourceForm
)


class CounselorRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access to counselors only"""

    def test_func(self):
        return hasattr(self.request.user, 'counselor_profile')


class ClientOrCounselorRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access to the client or assigned counselor only"""

    def test_func(self):
        obj = self.get_object()
        user = self.request.user

        # Allow access to the client
        if obj.client == user:
            return True

        # Allow access to the assigned counselor
        if hasattr(user, 'counselor_profile') and obj.counselor == user.counselor_profile:
            return True

        return False


# Counselor Views
class CounselorListView(LoginRequiredMixin, ListView):
    """View to list all available counselors"""
    model = Counselor
    template_name = 'counseling/counselor_list.html'
    context_object_name = 'counselors'

    def get_queryset(self):
        return Counselor.objects.filter(is_available=True)


class CounselorDetailView(LoginRequiredMixin, DetailView):
    """View to display counselor details"""
    model = Counselor
    template_name = 'counseling/counselor_detail.html'
    context_object_name = 'counselor'


class CounselorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update counselor profile"""
    model = Counselor
    form_class = CounselorForm
    template_name = 'counseling/counselor_form.html'
    success_url = reverse_lazy('counseling:counselor_dashboard')

    def test_func(self):
        counselor = self.get_object()
        return self.request.user == counselor.user


@login_required
def counselor_dashboard(request):
    """View for counselor's dashboard"""
    if not hasattr(request.user, 'counselor_profile'):
        messages.error(request, "You are not registered as a counselor.")
        return redirect('home')

    counselor = request.user.counselor_profile
    today = timezone.now().date()

    # Get upcoming sessions
    upcoming_sessions = Session.objects.filter(
        counselor=counselor,
        scheduled_at__date__gte=today,
        status__in=['scheduled', 'in_progress']
    ).order_by('scheduled_at')

    # Get recent sessions
    recent_sessions = Session.objects.filter(
        counselor=counselor,
        scheduled_at__date__lt=today
    ).order_by('-scheduled_at')[:5]

    # Get resources created by this counselor
    resources = Resource.objects.filter(created_by=counselor).order_by('-created_at')[:10]

    context = {
        'counselor': counselor,
        'upcoming_sessions': upcoming_sessions,
        'recent_sessions': recent_sessions,
        'resources': resources,
    }

    return render(request, 'counseling/counselor_dashboard.html', context)


# Session Views
class SessionListView(LoginRequiredMixin, ListView):
    """View to list sessions for a user"""
    model = Session
    template_name = 'counseling/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        user = self.request.user

        # If user is a counselor, show their sessions
        if hasattr(user, 'counselor_profile'):
            return Session.objects.filter(counselor=user.counselor_profile).order_by('-scheduled_at')
        else:
            # Otherwise show user's sessions as a client
            return Session.objects.filter(client=user).order_by('-scheduled_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        user = self.request.user

        # Split sessions into upcoming and past
        if hasattr(user, 'counselor_profile'):
            queryset = Session.objects.filter(counselor=user.counselor_profile)
        else:
            queryset = Session.objects.filter(client=user)

        context['upcoming_sessions'] = queryset.filter(
            scheduled_at__date__gte=today
        ).order_by('scheduled_at')

        context['past_sessions'] = queryset.filter(
            scheduled_at__date__lt=today
        ).order_by('-scheduled_at')

        return context


class SessionDetailView(LoginRequiredMixin, ClientOrCounselorRequiredMixin, DetailView):
    """View to display session details"""
    model = Session
    template_name = 'counseling/session_detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.object
        user = self.request.user

        # Add session notes if user is the counselor or if notes are not private
        if hasattr(user, 'counselor_profile') and session.counselor == user.counselor_profile:
            context['notes'] = session.notes.all()
            context['note_form'] = SessionNoteForm()
        else:
            context['notes'] = session.notes.filter(is_private=False)

        # Add shared resources
        context['shared_resources'] = session.shared_resources.all()

        # Add update form for counselors
        if hasattr(user, 'counselor_profile') and session.counselor == user.counselor_profile:
            context['update_form'] = SessionUpdateForm(instance=session)

        return context


class SessionCreateView(LoginRequiredMixin, CreateView):
    """View to create a new session"""
    model = Session
    form_class = SessionForm
    template_name = 'counseling/session_form.html'
    success_url = reverse_lazy('counseling:session_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        session = form.save(commit=False)

        # If the user is a client, set client to current user
        if not hasattr(self.request.user, 'counselor_profile'):
            session.client = self.request.user

        messages.success(self.request, "Session scheduled successfully!")
        return super().form_valid(form)


class SessionUpdateView(LoginRequiredMixin, ClientOrCounselorRequiredMixin, UpdateView):
    """View to update a session"""
    model = Session
    form_class = SessionUpdateForm
    template_name = 'counseling/session_update_form.html'

    def get_success_url(self):
        return reverse_lazy('counseling:session_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Session updated successfully!")
        return super().form_valid(form)


@login_required
def create_session_note(request, session_id):
    """View to create a note for a session"""
    session = get_object_or_404(Session, pk=session_id)

    # Only the counselor can create notes
    if not hasattr(request.user, 'counselor_profile') or session.counselor != request.user.counselor_profile:
        return HttpResponseForbidden("You don't have permission to add notes to this session.")

    if request.method == 'POST':
        form = SessionNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.session = session
            note.save()
            messages.success(request, "Note added successfully!")
        else:
            messages.error(request, "Error adding note.")

    return redirect('counseling:session_detail', pk=session_id)


# Resource Views
class ResourceListView(LoginRequiredMixin, ListView):
    """View to list resources"""
    model = Resource
    template_name = 'counseling/resource_list.html'
    context_object_name = 'resources'

    def get_queryset(self):
        user = self.request.user

        # If user is a counselor, show all their resources and public resources
        if hasattr(user, 'counselor_profile'):
            return Resource.objects.filter(
                Q(created_by=user.counselor_profile) | Q(is_public=True)
            ).distinct().order_by('-created_at')
        else:
            # If user is a client, show public resources and resources shared with them
            shared_resource_ids = SharedResource.objects.filter(
                client=user
            ).values_list('resource_id', flat=True)

            return Resource.objects.filter(
                Q(is_public=True) | Q(id__in=shared_resource_ids)
            ).distinct().order_by('-created_at')


class ResourceDetailView(LoginRequiredMixin, DetailView):
    """View to display resource details"""
    model = Resource
    template_name = 'counseling/resource_detail.html'
    context_object_name = 'resource'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        resource = self.object

        # Check if user has access to this resource
        has_access = resource.is_public

        if hasattr(user, 'counselor_profile'):
            has_access = has_access or resource.created_by == user.counselor_profile
        else:
            # Check if resource has been shared with this client
            has_access = has_access or SharedResource.objects.filter(
                resource=resource, client=user
            ).exists()

        context['has_access'] = has_access

        # For counselors, show clients with whom this resource has been shared
        if hasattr(user, 'counselor_profile') and resource.created_by == user.counselor_profile:
            context['shared_with'] = SharedResource.objects.filter(resource=resource)
            context['share_form'] = SharedResourceForm(counselor=user.counselor_profile)

        return context


class ResourceCreateView(LoginRequiredMixin, CounselorRequiredMixin, CreateView):
    """View to create a new resource"""
    model = Resource
    form_class = ResourceForm
    template_name = 'counseling/resource_form.html'

    def form_valid(self, form):
        resource = form.save(commit=False)
        resource.created_by = self.request.user.counselor_profile
        messages.success(self.request, "Resource created successfully!")
        return super().form_valid(form)


class ResourceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update a resource"""
    model = Resource
    form_class = ResourceForm
    template_name = 'counseling/resource_form.html'

    def test_func(self):
        resource = self.get_object()
        return hasattr(self.request.user,
                       'counselor_profile') and resource.created_by == self.request.user.counselor_profile

    def form_valid(self, form):
        messages.success(self.request, "Resource updated successfully!")
        return super().form_valid(form)


@login_required
def share_resource(request, resource_id):
    """View to share a resource with a client"""
    resource = get_object_or_404(Resource, pk=resource_id)

    # Check if user is a counselor and resource creator
    if not hasattr(request.user, 'counselor_profile') or resource.created_by != request.user.counselor_profile:
        return HttpResponseForbidden("You don't have permission to share this resource.")

    if request.method == 'POST':
        form = SharedResourceForm(request.POST, counselor=request.user.counselor_profile)
        if form.is_valid():
            shared_resource = form.save(commit=False)
            shared_resource.resource = resource
            shared_resource.save()
            messages.success(request, "Resource shared successfully!")
        else:
            messages.error(request, "Error sharing resource.")

    return redirect('counseling:resource_detail', pk=resource_id)