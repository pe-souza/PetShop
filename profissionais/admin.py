from django.contrib import admin
from .models import Profissional, HorarioDisponivel, Folga


class HorarioDisponivelInline(admin.TabularInline):
    model = HorarioDisponivel
    extra = 1


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'user', 'telefone', 'ativo', 'created_at']
    list_filter = ['ativo']
    search_fields = ['nome', 'user__username']
    inlines = [HorarioDisponivelInline]
    filter_horizontal = ['especialidades']


@admin.register(Folga)
class FolgaAdmin(admin.ModelAdmin):
    list_display = ['profissional', 'data', 'motivo']
    list_filter = ['profissional', 'data']
