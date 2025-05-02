from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string

from .models import Donation
from .forms import DonationForm


class DonationListView(ListView):
    """Display list of public donations"""
    model = Donation
    template_name = 'donations/donation_list.html'
    context_object_name = 'donations'
    paginate_by = 10

    def get_queryset(self):
        # Only show completed donations that aren't anonymous
        return Donation.objects.filter(
            status='completed',
            is_anonymous=False
        ).order_by('-created_at')


class DonationCreateView(CreateView):
    """View for creating a new donation"""
    model = Donation
    form_class = DonationForm
    template_name = 'donations/donate.html'
    success_url = reverse_lazy('donations:process_payment')

    def form_valid(self, form):
        donation = form.save(commit=False)

        # If user is logged in, associate donation with user
        if self.request.user.is_authenticated:
            donation.user = self.request.user
            if not donation.donor_name:
                donation.donor_name = self.request.user.get_full_name() or self.request.user.username
            if not donation.donor_email:
                donation.donor_email = self.request.user.email

        # Generate a transaction ID
        donation.transaction_id = get_random_string(length=16)
        donation.save()

        # Store donation ID in session to retrieve it on payment page
        self.request.session['donation_id'] = donation.id

        return super().form_valid(form)


def process_payment(request):
    """Process payment for donation"""
    # In a real application, this would integrate with a payment gateway
    donation_id = request.session.get('donation_id')

    if not donation_id:
        messages.error(request, "No donation to process.")
        return redirect('donations:donate')

    try:
        donation = Donation.objects.get(id=donation_id)
    except Donation.DoesNotExist:
        messages.error(request, "Donation not found.")
        return redirect('donations:donate')

    # This is a simplified payment process
    # In a real application, redirect to payment gateway

    # For demonstration, simulate successful payment
    if request.method == 'POST':
        # Simulate successful payment
        donation.status = 'completed'
        donation.save()

        # Clear session
        if 'donation_id' in request.session:
            del request.session['donation_id']

        messages.success(request, "Thank you for your donation!")
        return redirect('donations:donation_success', pk=donation.id)

    return render(request, 'donations/process_payment.html', {'donation': donation})


class DonationSuccessView(DetailView):
    """Display donation confirmation"""
    model = Donation
    template_name = 'donations/donation_success.html'
    context_object_name = 'donation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Donation Successful'
        return context


class UserDonationHistoryView(LoginRequiredMixin, ListView):
    """Display donation history for logged-in user"""
    model = Donation
    template_name = 'donations/donation_history.html'
    context_object_name = 'donations'
    paginate_by = 10

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user).order_by('-created_at')
