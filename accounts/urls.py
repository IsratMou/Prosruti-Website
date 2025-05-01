from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignupOptionsView.as_view(), name='signup_options'),
    path('signup/survivor/', views.SurvivorSignUpView.as_view(), name='survivor_signup'),
    path('signup/counselor/', views.CounselorSignUpView.as_view(), name='counselor_signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]