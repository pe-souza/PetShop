from django.urls import path
from django.shortcuts import render
from .models import Service

app_name = 'servicos'


def services_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/services_list.html', {'services': services})


urlpatterns = [
    path('', services_list, name='list'),
]
