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
    path('sessions/<int:pk>/update/', views.SessionUpdateView.as_view(), name='session_update'),
    path('sessions/<int:session_id>/notes/add/', views.create_session_note, name='create_session_note'),

    # Resource URLs
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('resources/create/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('resources/<int:pk>/update/', views.ResourceUpdateView.as_view(), name='resource_update'),
    path('resources/<int:resource_id>/share/', views.share_resource, name='share_resource'),
]