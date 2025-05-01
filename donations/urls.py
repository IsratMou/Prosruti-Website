from django.urls import path
from django.http import HttpResponse

def empty_view(request):
    return HttpResponse("Donations coming soon")

urlpatterns = [
    path('', empty_view, name='donations_home'),
]
