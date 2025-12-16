from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'email', 'ativo', 'created_at']
    list_filter = ['ativo', 'cidade']
    search_fields = ['nome', 'telefone', 'email', 'cpf']
