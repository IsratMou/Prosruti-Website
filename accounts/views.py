from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import LoginForm, UserSignUpForm, CounselorSignUpForm
from .models import CustomUser

class HomeView(TemplateView):
    template_name = 'home.html'

class SignupOptionsView(TemplateView):
    template_name = 'accounts/login_options.html'

class SurvivorSignUpView(CreateView):
    model = CustomUser
    form_class = UserSignUpForm
    template_name = 'accounts/register_user.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Account created successfully. Please log in.')
        return super().form_valid(form)

class CounselorSignUpView(CreateView):
    model = CustomUser
    form_class = CounselorSignUpForm
    template_name = 'accounts/register_counselor.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Counselor account created successfully. Your account will be reviewed shortly.')
        return super().form_valid(form)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Welcome back, {username}!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username or password')
            return self.form_invalid(form)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard_view(request):
    user_type = request.user.user_type
    if user_type == 'survivor':
        return render(request, 'accounts/user_dashboard.html')
    elif user_type == 'counselor':
        return render(request, 'accounts/counselor_dashboard.html')
    else:
        return redirect('home')