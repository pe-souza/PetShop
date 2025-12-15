from django.shortcuts import render
from .models import Service

def services_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/services_list.html', {'services': services})
