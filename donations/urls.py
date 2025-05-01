from django.urls import path
from . import views

app_name = 'counseling'

urlpatterns = [
    # Counselor URLs
    path('counselors/', views.CounselorListView.as_view(), name='counselor_list'),
    path('counselors/<int:pk>/', views.CounselorDetailView.as_view(), name='counselor_detail'),
    path('counselors/<int:pk>/update/', views.CounselorUpdateView.as_view(), name='counselor_update'),
    path('dashboard/', views.counselor_dashboard, name='counselor_dashboard'),

    # Session URLs
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('sessions/<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('sessions/create/', views.SessionCreateView.as_view(), name='session_create'),