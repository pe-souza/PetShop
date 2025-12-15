from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    path('services/', views.services_list, name='services_list'),
    path('services/create/', views.services_create, name='services_create'),
    path('services/<int:pk>/edit/', views.services_edit, name='services_edit'),
    path('services/<int:pk>/delete/', views.services_delete, name='services_delete'),
    path('services/<int:pk>/toggle/', views.services_toggle, name='services_toggle'),
    
    path('testimonials/', views.testimonials_list, name='testimonials_list'),
    path('testimonials/<int:pk>/', views.testimonials_detail, name='testimonials_detail'),
    path('testimonials/<int:pk>/approve/', views.testimonials_approve, name='testimonials_approve'),
    path('testimonials/<int:pk>/reject/', views.testimonials_reject, name='testimonials_reject'),
    path('testimonials/<int:pk>/delete/', views.testimonials_delete, name='testimonials_delete'),
]
