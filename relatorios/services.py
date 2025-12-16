from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncDate
from datetime import date, timedelta
from agendamentos.models import Agendamento, HistoricoAtendimento
from clientes.models import Cliente
from pets.models import Pet
from servicos.models import Service


def get_dashboard_stats():
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)
    
    return {
        'total_clientes': Cliente.objects.filter(ativo=True).count(),
        'total_pets': Pet.objects.filter(ativo=True).count(),
        'agendamentos_hoje': Agendamento.objects.filter(data=hoje, status__in=['agendado', 'confirmado']).count(),
        'agendamentos_mes': Agendamento.objects.filter(data__gte=inicio_mes, status__in=['agendado', 'confirmado', 'concluido']).count(),
        'faturamento_mes': Agendamento.objects.filter(data__gte=inicio_mes, status='concluido').aggregate(total=Sum('preco'))['total'] or 0,
        'servicos_ativos': Service.objects.filter(is_active=True).count(),
    }


def get_agendamentos_por_periodo(data_inicio, data_fim):
    return Agendamento.objects.filter(
        data__gte=data_inicio,
        data__lte=data_fim
    ).values('data').annotate(
        total=Count('id'),
        faturamento=Sum('preco')
    ).order_by('data')


def get_servicos_mais_utilizados(data_inicio=None, data_fim=None, limit=10):
    queryset = Agendamento.objects.filter(status='concluido')
    
    if data_inicio:
        queryset = queryset.filter(data__gte=data_inicio)
    if data_fim:
        queryset = queryset.filter(data__lte=data_fim)
    
    return queryset.values('servico__name').annotate(
        total=Count('id'),
        faturamento=Sum('preco')
    ).order_by('-total')[:limit]


def get_faturamento_mensal(ano=None):
    if not ano:
        ano = date.today().year
    
    return Agendamento.objects.filter(
        data__year=ano,
        status='concluido'
    ).annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(
        total=Sum('preco'),
        quantidade=Count('id')
    ).order_by('mes')


def get_profissionais_ranking(data_inicio=None, data_fim=None, limit=10):
    queryset = Agendamento.objects.filter(status='concluido', profissional__isnull=False)
    
    if data_inicio:
        queryset = queryset.filter(data__gte=data_inicio)
    if data_fim:
        queryset = queryset.filter(data__lte=data_fim)
    
    return queryset.values('profissional__nome').annotate(
        total_atendimentos=Count('id'),
        faturamento=Sum('preco')
    ).order_by('-total_atendimentos')[:limit]


def get_clientes_frequentes(limit=10):
    return Cliente.objects.filter(ativo=True).annotate(
        total_agendamentos=Count('agendamentos')
    ).order_by('-total_agendamentos')[:limit]


def get_proximos_agendamentos(limit=10):
    hoje = date.today()
    return Agendamento.objects.filter(
        data__gte=hoje,
        status__in=['agendado', 'confirmado']
    ).select_related('cliente', 'pet', 'servico', 'profissional').order_by('data', 'hora_inicio')[:limit]
