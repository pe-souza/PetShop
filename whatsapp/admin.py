from django.contrib import admin
from .models import MensagemTemplate, MensagemEnviada


@admin.register(MensagemTemplate)
class MensagemTemplateAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'ativo', 'created_at']
    list_filter = ['tipo', 'ativo']


@admin.register(MensagemEnviada)
class MensagemEnviadaAdmin(admin.ModelAdmin):
    list_display = ['agendamento', 'telefone', 'status', 'enviada_em', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['telefone', 'mensagem']
