from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.DonationCreateView.as_view(), name='donate'),
    path('list/', views.DonationListView.as_view(), name='donation_list'),
    path('process/', views.process_payment, name='process_payment'),
    path('success/<int:pk>/', views.DonationSuccessView.as_view(), name='donation_success'),
    path('history/', views.UserDonationHistoryView.as_view(), name='donation_history'),
]

