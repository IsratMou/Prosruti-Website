from django.urls import path
from . import views

app_name = 'counseling'

urlpatterns = [
    # Counselor URLs
    path('counselors/', views.CounselorListView.as_view(), name='counselor_list'),
    path('counselors/<int:pk>/', views.CounselorDetailView.as_view(), name='counselor_detail'),
    path('counselors/<int:pk>/update/', views.CounselorUpdateView.as_view(), name='counselor_update'),
    path('dashboard/', views.counselor_dashboard, name='counselor_dashboard'),