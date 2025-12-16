from django.contrib import admin
from .models import Service, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['ativo']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'categoria', 'price', 'duracao_minutos', 'is_active', 'created_at']
    list_filter = ['is_active', 'categoria', 'porte_aplicavel']
    search_fields = ['name', 'description']
