from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from servicos.models import Service
from clientes.models import Cliente
from pets.models import Pet
from profissionais.models import Profissional, HorarioDisponivel, Folga
from agendamentos.models import Agendamento


def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, 'pages/home.html', {'services': services})


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')


def agendar_online(request):
    servicos = Service.objects.filter(is_active=True)
    profissionais = Profissional.objects.filter(ativo=True)
    
    context = {
        'servicos': servicos,
        'profissionais': profissionais,
    }
    return render(request, 'pages/agendar.html', context)


def get_horarios_disponiveis(request):
    data_str = request.GET.get('data')
    profissional_id = request.GET.get('profissional')
    servico_id = request.GET.get('servico')
    
    if not all([data_str, profissional_id, servico_id]):
        return JsonResponse({'horarios': []})
    
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        profissional = Profissional.objects.get(pk=profissional_id, ativo=True)
        servico = Service.objects.get(pk=servico_id, is_active=True)
    except (ValueError, Profissional.DoesNotExist, Service.DoesNotExist):
        return JsonResponse({'horarios': []})
    
    if Folga.objects.filter(profissional=profissional, data=data).exists():
        return JsonResponse({'horarios': []})
    
    dia_semana = data.weekday()
    horarios_profissional = HorarioDisponivel.objects.filter(
        profissional=profissional,
        dia_semana=dia_semana,
        ativo=True
    )
    
    if not horarios_profissional.exists():
        return JsonResponse({'horarios': []})
    
    agendamentos_dia = Agendamento.objects.filter(
        profissional=profissional,
        data=data,
        status__in=['agendado', 'confirmado', 'em_andamento']
    )
    
    horarios_ocupados = [(a.hora_inicio, a.hora_fim) for a in agendamentos_dia]
    
    horarios_disponiveis = []
    duracao = timedelta(minutes=servico.duracao_minutos)
    
    for h in horarios_profissional:
        hora_atual = datetime.combine(data, h.hora_inicio)
        hora_fim_periodo = datetime.combine(data, h.hora_fim)
        
        while hora_atual + duracao <= hora_fim_periodo:
            hora_inicio = hora_atual.time()
            hora_fim = (hora_atual + duracao).time()
            
            conflito = False
            for ocupado_inicio, ocupado_fim in horarios_ocupados:
                if hora_inicio < ocupado_fim and hora_fim > ocupado_inicio:
                    conflito = True
                    break
            
            if not conflito:
                horarios_disponiveis.append(hora_inicio.strftime('%H:%M'))
            
            hora_atual += timedelta(minutes=30)
    
    return JsonResponse({'horarios': horarios_disponiveis})


def criar_agendamento_online(request):
    if request.method != 'POST':
        return redirect('pages:agendar_online')
    
    nome = request.POST.get('nome')
    telefone = request.POST.get('telefone')
    email = request.POST.get('email', '')
    pet_nome = request.POST.get('pet_nome')
    pet_especie = request.POST.get('pet_especie', 'cachorro')
    pet_porte = request.POST.get('pet_porte', 'pequeno')
    servico_id = request.POST.get('servico')
    profissional_id = request.POST.get('profissional')
    data_str = request.POST.get('data')
    hora_str = request.POST.get('hora')
    observacoes = request.POST.get('observacoes', '')
    
    try:
        cliente, created = Cliente.objects.get_or_create(
            telefone=telefone,
            defaults={'nome': nome, 'email': email}
        )
        if not created and not cliente.nome:
            cliente.nome = nome
            cliente.save()
        
        pet, created = Pet.objects.get_or_create(
            cliente=cliente,
            nome=pet_nome,
            defaults={'especie': pet_especie, 'porte': pet_porte}
        )
        
        servico = Service.objects.get(pk=servico_id)
        profissional = Profissional.objects.get(pk=profissional_id) if profissional_id else None
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()
        
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            pet=pet,
            servico=servico,
            profissional=profissional,
            data=data,
            hora_inicio=hora,
            preco=servico.get_preco_por_porte(pet_porte),
            observacoes=observacoes,
            status='agendado'
        )
        
        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('pages:agendar_sucesso')
        
    except Exception as e:
        messages.error(request, f'Erro ao realizar agendamento. Por favor, tente novamente.')
        return redirect('pages:agendar_online')


def agendar_sucesso(request):
    return render(request, 'pages/agendar_sucesso.html')
