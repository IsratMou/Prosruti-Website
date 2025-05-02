from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignupOptionsView.as_view(), name='login_options'),
    path('register/user/', views.SurvivorSignUpView.as_view(), name='register_user'),
    path('register/counselor/', views.CounselorSignUpView.as_view(), name='register_counselor'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]