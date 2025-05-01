from django.urls import path
from django.http import HttpResponse

def empty_view(request):
    return HttpResponse("This section is under construction")

urlpatterns = [
    path('', empty_view, name='counseling_home'),
]