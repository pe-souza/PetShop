from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.services.models import Service
from .models import Testimonial
from .forms import ServiceForm, TestimonialForm
from .decorators import admin_required

def admin_login(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request, 'Você não tem permissão de administrador.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'admin_panel/login.html')

def admin_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('admin_panel:login')

@admin_required
def dashboard(request):
    services_count = Service.objects.count()
    active_services = Service.objects.filter(is_active=True).count()
    testimonials_count = Testimonial.objects.count()
    pending_testimonials = Testimonial.objects.filter(status='pending').count()
    
    context = {
        'services_count': services_count,
        'active_services': active_services,
        'testimonials_count': testimonials_count,
        'pending_testimonials': pending_testimonials,
        'recent_services': Service.objects.order_by('-created_at')[:5],
        'recent_testimonials': Testimonial.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)

@admin_required
def services_list(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/services/list.html', {'services': services})

@admin_required
def services_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço criado com sucesso!')
            return redirect('admin_panel:services_list')
    else:
        form = ServiceForm()
    return render(request, 'admin_panel/services/create.html', {'form': form})

@admin_required
def services_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('admin_panel:services_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'admin_panel/services/edit.html', {'form': form, 'service': service})

@admin_required
def services_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Serviço excluído com sucesso!')
        return redirect('admin_panel:services_list')
    return render(request, 'admin_panel/services/delete.html', {'service': service})

@admin_required
def services_toggle(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.is_active = not service.is_active
    service.save()
    status = 'ativado' if service.is_active else 'desativado'
    messages.success(request, f'Serviço {status} com sucesso!')
    return redirect('admin_panel:services_list')

@admin_required
def testimonials_list(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/testimonials/list.html', {'testimonials': testimonials})

@admin_required
def testimonials_detail(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    return render(request, 'admin_panel/testimonials/detail.html', {'testimonial': testimonial})

@admin_required
def testimonials_approve(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.status = 'approved'
    testimonial.save()
    messages.success(request, 'Depoimento aprovado com sucesso!')
    return redirect('admin_panel:testimonials_list')

@admin_required
def testimonials_reject(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.status = 'rejected'
    testimonial.save()
    messages.success(request, 'Depoimento reprovado.')
    return redirect('admin_panel:testimonials_list')

@admin_required
def testimonials_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Depoimento excluído com sucesso!')
        return redirect('admin_panel:testimonials_list')
    return render(request, 'admin_panel/testimonials/delete.html', {'testimonial': testimonial})
