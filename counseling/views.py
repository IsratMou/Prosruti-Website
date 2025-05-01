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