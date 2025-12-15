from django.shortcuts import render
from apps.services.models import Service

def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, 'pages/home.html', {'services': services})

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')
