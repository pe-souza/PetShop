from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/novo/', views.clientes_create, name='clientes_create'),
    path('clientes/<int:pk>/', views.clientes_detail, name='clientes_detail'),
    path('clientes/<int:pk>/editar/', views.clientes_edit, name='clientes_edit'),
    
    path('pets/', views.pets_list, name='pets_list'),
    path('pets/novo/', views.pets_create, name='pets_create'),
    path('pets/<int:pk>/', views.pets_detail, name='pets_detail'),
    path('pets/<int:pk>/editar/', views.pets_edit, name='pets_edit'),
    path('api/pets/', views.get_pets_cliente, name='get_pets_cliente'),
    
    path('services/', views.services_list, name='services_list'),
    path('services/create/', views.services_create, name='services_create'),
    path('services/<int:pk>/edit/', views.services_edit, name='services_edit'),
    path('services/<int:pk>/delete/', views.services_delete, name='services_delete'),
    path('services/<int:pk>/toggle/', views.services_toggle, name='services_toggle'),
    
    path('profissionais/', views.profissionais_list, name='profissionais_list'),
    path('profissionais/novo/', views.profissionais_create, name='profissionais_create'),
    path('profissionais/<int:pk>/editar/', views.profissionais_edit, name='profissionais_edit'),
    path('profissionais/<int:pk>/horarios/', views.profissionais_horarios, name='profissionais_horarios'),
    path('profissionais/<int:pk>/folgas/', views.profissionais_folgas, name='profissionais_folgas'),
    
    path('agenda/', views.agenda, name='agenda'),
    path('agenda/json/', views.agenda_json, name='agenda_json'),
    
    path('agendamentos/', views.agendamentos_list, name='agendamentos_list'),
    path('agendamentos/novo/', views.agendamentos_create, name='agendamentos_create'),
    path('agendamentos/<int:pk>/editar/', views.agendamentos_edit, name='agendamentos_edit'),
    path('agendamentos/<int:pk>/status/<str:status>/', views.agendamentos_status, name='agendamentos_status'),
    
    path('relatorios/', views.relatorios_view, name='relatorios'),
    
    path('whatsapp/', views.whatsapp_config, name='whatsapp_config'),
    
    path('testimonials/', views.testimonials_list, name='testimonials_list'),
    path('testimonials/<int:pk>/', views.testimonials_detail, name='testimonials_detail'),
    path('testimonials/<int:pk>/approve/', views.testimonials_approve, name='testimonials_approve'),
    path('testimonials/<int:pk>/reject/', views.testimonials_reject, name='testimonials_reject'),
    path('testimonials/<int:pk>/delete/', views.testimonials_delete, name='testimonials_delete'),
]
