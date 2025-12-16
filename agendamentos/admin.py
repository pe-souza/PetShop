from django.contrib import admin
from .models import Agendamento, HistoricoAtendimento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['pet', 'servico', 'profissional', 'data', 'hora_inicio', 'status', 'preco']
    list_filter = ['status', 'data', 'profissional', 'servico']
    search_fields = ['pet__nome', 'cliente__nome', 'servico__name']
    date_hierarchy = 'data'


@admin.register(HistoricoAtendimento)
class HistoricoAtendimentoAdmin(admin.ModelAdmin):
    list_display = ['pet', 'servico', 'profissional', 'data_atendimento', 'valor_cobrado']
    list_filter = ['data_atendimento', 'profissional', 'servico']
    search_fields = ['pet__nome', 'servico__name']
