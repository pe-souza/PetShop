from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cliente', 'especie', 'raca', 'porte', 'ativo']
    list_filter = ['especie', 'porte', 'ativo']
    search_fields = ['nome', 'cliente__nome', 'raca']
