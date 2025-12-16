from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta
import json

from servicos.models import Service, Categoria
from clientes.models import Cliente
from pets.models import Pet
from profissionais.models import Profissional, HorarioDisponivel, Folga
from agendamentos.models import Agendamento, HistoricoAtendimento
from whatsapp.models import MensagemTemplate, MensagemEnviada
from whatsapp.services import enviar_confirmacao_agendamento, enviar_cancelamento
from relatorios.services import get_dashboard_stats, get_servicos_mais_utilizados, get_proximos_agendamentos

from .models import Testimonial
from .forms import (ServiceForm, CategoriaForm, ClienteForm, PetForm, 
                    ProfissionalForm, HorarioDisponivelForm, FolgaForm,
                    AgendamentoForm, MensagemTemplateForm, TestimonialForm)
from .decorators import admin_required, staff_required


def admin_login(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request, 'Você não tem permissão de acesso.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('admin_panel:login')


@staff_required
def dashboard(request):
    stats = get_dashboard_stats()
    servicos_populares = get_servicos_mais_utilizados(limit=5)
    proximos_agendamentos = get_proximos_agendamentos(limit=8)
    
    context = {
        **stats,
        'servicos_populares': servicos_populares,
        'proximos_agendamentos': proximos_agendamentos,
        'recent_services': Service.objects.order_by('-created_at')[:5],
        'pending_testimonials': Testimonial.objects.filter(status='pending').count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@staff_required
def clientes_list(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.all()
    if query:
        clientes = clientes.filter(nome__icontains=query) | clientes.filter(telefone__icontains=query)
    
    paginator = Paginator(clientes, 20)
    page = request.GET.get('page')
    clientes = paginator.get_page(page)
    
    return render(request, 'admin_panel/clientes/list.html', {'clientes': clientes, 'query': query})


@staff_required
def clientes_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('admin_panel:clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'admin_panel/clientes/form.html', {'form': form, 'titulo': 'Novo Cliente'})


@staff_required
def clientes_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('admin_panel:clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'admin_panel/clientes/form.html', {'form': form, 'cliente': cliente, 'titulo': 'Editar Cliente'})


@staff_required
def clientes_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    pets = cliente.pets.all()
    agendamentos = cliente.agendamentos.order_by('-data', '-hora_inicio')[:10]
    return render(request, 'admin_panel/clientes/detail.html', {'cliente': cliente, 'pets': pets, 'agendamentos': agendamentos})


@staff_required
def pets_list(request):
    query = request.GET.get('q', '')
    pets = Pet.objects.select_related('cliente').all()
    if query:
        pets = pets.filter(nome__icontains=query) | pets.filter(cliente__nome__icontains=query)
    
    paginator = Paginator(pets, 20)
    page = request.GET.get('page')
    pets = paginator.get_page(page)
    
    return render(request, 'admin_panel/pets/list.html', {'pets': pets, 'query': query})


@staff_required
def pets_create(request):
    cliente_id = request.GET.get('cliente')
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet cadastrado com sucesso!')
            return redirect('admin_panel:pets_list')
    else:
        form = PetForm()
        if cliente_id:
            form.fields['cliente'].initial = cliente_id
    return render(request, 'admin_panel/pets/form.html', {'form': form, 'titulo': 'Novo Pet'})


@staff_required
def pets_edit(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet atualizado com sucesso!')
            return redirect('admin_panel:pets_list')
    else:
        form = PetForm(instance=pet)
    return render(request, 'admin_panel/pets/form.html', {'form': form, 'pet': pet, 'titulo': 'Editar Pet'})


@staff_required
def pets_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    historico = pet.agendamentos.order_by('-data', '-hora_inicio')[:10]
    return render(request, 'admin_panel/pets/detail.html', {'pet': pet, 'historico': historico})


@staff_required
def services_list(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/services/list.html', {'services': services})


@staff_required
def services_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço criado com sucesso!')
            return redirect('admin_panel:services_list')
    else:
        form = ServiceForm()
    return render(request, 'admin_panel/services/form.html', {'form': form, 'titulo': 'Novo Serviço'})


@staff_required
def services_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('admin_panel:services_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'admin_panel/services/form.html', {'form': form, 'service': service, 'titulo': 'Editar Serviço'})


@staff_required
def services_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Serviço excluído com sucesso!')
        return redirect('admin_panel:services_list')
    return render(request, 'admin_panel/services/delete.html', {'service': service})


@staff_required
def services_toggle(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.is_active = not service.is_active
    service.save()
    status = 'ativado' if service.is_active else 'desativado'
    messages.success(request, f'Serviço {status} com sucesso!')
    return redirect('admin_panel:services_list')


@staff_required
def profissionais_list(request):
    profissionais = Profissional.objects.all()
    return render(request, 'admin_panel/profissionais/list.html', {'profissionais': profissionais})


@admin_required
def profissionais_create(request):
    if request.method == 'POST':
        form = ProfissionalForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            is_admin = request.POST.get('is_admin') == 'on'
            
            if username and password:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    is_staff=True,
                    is_superuser=is_admin
                )
            else:
                user = User.objects.create_user(
                    username=f"prof_{datetime.now().timestamp()}",
                    password=User.objects.make_random_password(),
                    is_staff=True
                )
            
            profissional = form.save(commit=False)
            profissional.user = user
            profissional.save()
            form.save_m2m()
            
            messages.success(request, 'Profissional cadastrado com sucesso!')
            return redirect('admin_panel:profissionais_list')
    else:
        form = ProfissionalForm()
    return render(request, 'admin_panel/profissionais/form.html', {'form': form, 'titulo': 'Novo Profissional'})


@admin_required
def profissionais_edit(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    if request.method == 'POST':
        form = ProfissionalForm(request.POST, request.FILES, instance=profissional)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profissional atualizado com sucesso!')
            return redirect('admin_panel:profissionais_list')
    else:
        form = ProfissionalForm(instance=profissional)
    return render(request, 'admin_panel/profissionais/form.html', {'form': form, 'profissional': profissional, 'titulo': 'Editar Profissional'})


@staff_required
def profissionais_horarios(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    horarios = profissional.horarios.all()
    
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.profissional = profissional
            horario.save()
            messages.success(request, 'Horário adicionado com sucesso!')
            return redirect('admin_panel:profissionais_horarios', pk=pk)
    else:
        form = HorarioDisponivelForm()
    
    return render(request, 'admin_panel/profissionais/horarios.html', {
        'profissional': profissional,
        'horarios': horarios,
        'form': form
    })


@staff_required
def profissionais_folgas(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    folgas = profissional.folgas.filter(data__gte=date.today())
    
    if request.method == 'POST':
        form = FolgaForm(request.POST)
        if form.is_valid():
            folga = form.save(commit=False)
            folga.profissional = profissional
            folga.save()
            messages.success(request, 'Folga registrada com sucesso!')
            return redirect('admin_panel:profissionais_folgas', pk=pk)
    else:
        form = FolgaForm()
    
    return render(request, 'admin_panel/profissionais/folgas.html', {
        'profissional': profissional,
        'folgas': folgas,
        'form': form
    })


@staff_required
def agenda(request):
    data_str = request.GET.get('data', date.today().strftime('%Y-%m-%d'))
    visualizacao = request.GET.get('view', 'dia')
    profissional_id = request.GET.get('profissional')
    
    try:
        data_atual = datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        data_atual = date.today()
    
    profissionais = Profissional.objects.filter(ativo=True)
    
    if visualizacao == 'dia':
        data_inicio = data_atual
        data_fim = data_atual
    elif visualizacao == 'semana':
        data_inicio = data_atual - timedelta(days=data_atual.weekday())
        data_fim = data_inicio + timedelta(days=6)
    else:
        data_inicio = data_atual.replace(day=1)
        if data_atual.month == 12:
            data_fim = data_atual.replace(year=data_atual.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            data_fim = data_atual.replace(month=data_atual.month + 1, day=1) - timedelta(days=1)
    
    agendamentos = Agendamento.objects.filter(
        data__gte=data_inicio,
        data__lte=data_fim
    ).select_related('cliente', 'pet', 'servico', 'profissional')
    
    if profissional_id:
        agendamentos = agendamentos.filter(profissional_id=profissional_id)
    
    context = {
        'agendamentos': agendamentos,
        'profissionais': profissionais,
        'data_atual': data_atual,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'visualizacao': visualizacao,
        'profissional_selecionado': profissional_id,
    }
    return render(request, 'admin_panel/agenda/calendario.html', context)


@staff_required
def agenda_json(request):
    data_inicio = request.GET.get('start', date.today().strftime('%Y-%m-%d'))
    data_fim = request.GET.get('end', (date.today() + timedelta(days=30)).strftime('%Y-%m-%d'))
    
    agendamentos = Agendamento.objects.filter(
        data__gte=data_inicio,
        data__lte=data_fim,
        status__in=['agendado', 'confirmado', 'em_andamento']
    ).select_related('cliente', 'pet', 'servico', 'profissional')
    
    eventos = []
    for a in agendamentos:
        eventos.append({
            'id': a.id,
            'title': f'{a.pet.nome} - {a.servico.name}',
            'start': f'{a.data}T{a.hora_inicio}',
            'end': f'{a.data}T{a.hora_fim}' if a.hora_fim else None,
            'color': a.profissional.cor_agenda if a.profissional else '#7C3AED',
            'extendedProps': {
                'cliente': a.cliente.nome,
                'pet': a.pet.nome,
                'servico': a.servico.name,
                'profissional': a.profissional.nome if a.profissional else 'Não definido',
                'status': a.get_status_display(),
                'preco': str(a.preco),
            }
        })
    
    return JsonResponse(eventos, safe=False)


@staff_required
def agendamentos_list(request):
    status_filter = request.GET.get('status', '')
    data_filter = request.GET.get('data', '')
    
    agendamentos = Agendamento.objects.select_related('cliente', 'pet', 'servico', 'profissional').all()
    
    if status_filter:
        agendamentos = agendamentos.filter(status=status_filter)
    if data_filter:
        agendamentos = agendamentos.filter(data=data_filter)
    
    paginator = Paginator(agendamentos.order_by('-data', '-hora_inicio'), 20)
    page = request.GET.get('page')
    agendamentos = paginator.get_page(page)
    
    return render(request, 'admin_panel/agendamentos/list.html', {
        'agendamentos': agendamentos,
        'status_filter': status_filter,
        'data_filter': data_filter,
        'status_choices': Agendamento.STATUS_CHOICES,
    })


@staff_required
def agendamentos_create(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.criado_por = request.user
            agendamento.save()
            
            enviar_confirmacao_agendamento(agendamento)
            
            messages.success(request, 'Agendamento criado com sucesso!')
            return redirect('admin_panel:agenda')
    else:
        form = AgendamentoForm()
    return render(request, 'admin_panel/agendamentos/form.html', {'form': form, 'titulo': 'Novo Agendamento'})


@staff_required
def agendamentos_edit(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('admin_panel:agenda')
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'admin_panel/agendamentos/form.html', {'form': form, 'agendamento': agendamento, 'titulo': 'Editar Agendamento'})


@staff_required
def agendamentos_status(request, pk, status):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if status in dict(Agendamento.STATUS_CHOICES):
        agendamento.status = status
        agendamento.save()
        
        if status == 'cancelado':
            enviar_cancelamento(agendamento)
        
        if status == 'concluido':
            HistoricoAtendimento.objects.create(
                agendamento=agendamento,
                pet=agendamento.pet,
                servico=agendamento.servico,
                profissional=agendamento.profissional,
                data_atendimento=datetime.now(),
                valor_cobrado=agendamento.preco,
                observacoes=agendamento.observacoes
            )
        
        messages.success(request, f'Status atualizado para: {agendamento.get_status_display()}')
    
    return redirect('admin_panel:agenda')


@staff_required
def get_pets_cliente(request):
    cliente_id = request.GET.get('cliente_id')
    if cliente_id:
        pets = Pet.objects.filter(cliente_id=cliente_id, ativo=True).values('id', 'nome')
        return JsonResponse(list(pets), safe=False)
    return JsonResponse([], safe=False)


@staff_required
def relatorios_view(request):
    from relatorios.services import get_faturamento_mensal, get_profissionais_ranking, get_clientes_frequentes
    
    stats = get_dashboard_stats()
    servicos_populares = get_servicos_mais_utilizados(limit=10)
    faturamento_mensal = list(get_faturamento_mensal())
    profissionais_ranking = get_profissionais_ranking(limit=10)
    clientes_frequentes = get_clientes_frequentes(limit=10)
    
    context = {
        **stats,
        'servicos_populares': servicos_populares,
        'faturamento_mensal': faturamento_mensal,
        'profissionais_ranking': profissionais_ranking,
        'clientes_frequentes': clientes_frequentes,
    }
    return render(request, 'admin_panel/relatorios/dashboard.html', context)


@admin_required
def whatsapp_config(request):
    templates = MensagemTemplate.objects.all()
    mensagens_recentes = MensagemEnviada.objects.order_by('-created_at')[:20]
    
    if request.method == 'POST':
        form = MensagemTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Template salvo com sucesso!')
            return redirect('admin_panel:whatsapp_config')
    else:
        form = MensagemTemplateForm()
    
    return render(request, 'admin_panel/whatsapp/config.html', {
        'templates': templates,
        'mensagens_recentes': mensagens_recentes,
        'form': form,
    })


@staff_required
def testimonials_list(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/testimonials/list.html', {'testimonials': testimonials})


@staff_required
def testimonials_detail(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    return render(request, 'admin_panel/testimonials/detail.html', {'testimonial': testimonial})


@staff_required
def testimonials_approve(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.status = 'approved'
    testimonial.save()
    messages.success(request, 'Depoimento aprovado com sucesso!')
    return redirect('admin_panel:testimonials_list')


@staff_required
def testimonials_reject(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.status = 'rejected'
    testimonial.save()
    messages.success(request, 'Depoimento reprovado.')
    return redirect('admin_panel:testimonials_list')


@staff_required
def testimonials_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Depoimento excluído com sucesso!')
        return redirect('admin_panel:testimonials_list')
    return render(request, 'admin_panel/testimonials/delete.html', {'testimonial': testimonial})
