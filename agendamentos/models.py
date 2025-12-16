from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from clientes.models import Cliente
from pets.models import Pet
from servicos.models import Service
from profissionais.models import Profissional


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('nao_compareceu', 'Não Compareceu'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Cliente')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Pet')
    servico = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Serviço')
    profissional = models.ForeignKey(Profissional, on_delete=models.SET_NULL, null=True, blank=True, related_name='agendamentos', verbose_name='Profissional')
    data = models.DateField('Data')
    hora_inicio = models.TimeField('Hora Início')
    hora_fim = models.TimeField('Hora Fim', blank=True, null=True)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='agendado')
    observacoes = models.TextField('Observações', blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agendamentos_criados', verbose_name='Criado por')
    whatsapp_confirmacao_enviada = models.BooleanField('Confirmação WhatsApp enviada', default=False)
    whatsapp_lembrete_enviado = models.BooleanField('Lembrete WhatsApp enviado', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data', '-hora_inicio']

    def __str__(self):
        return f'{self.pet.nome} - {self.servico.name} - {self.data}'
    
    def save(self, *args, **kwargs):
        if not self.hora_fim and self.hora_inicio and self.servico:
            inicio = datetime.combine(self.data, self.hora_inicio)
            fim = inicio + timedelta(minutes=self.servico.duracao_minutos)
            self.hora_fim = fim.time()
        if not self.preco and self.servico:
            self.preco = self.servico.get_preco_por_porte(self.pet.porte or 'pequeno')
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.profissional and self.data and self.hora_inicio:
            conflitos = Agendamento.objects.filter(
                profissional=self.profissional,
                data=self.data,
                status__in=['agendado', 'confirmado', 'em_andamento']
            ).exclude(pk=self.pk)
            
            hora_fim = self.hora_fim
            if not hora_fim and self.servico:
                inicio = datetime.combine(self.data, self.hora_inicio)
                fim = inicio + timedelta(minutes=self.servico.duracao_minutos)
                hora_fim = fim.time()
            
            for agendamento in conflitos:
                if (self.hora_inicio < agendamento.hora_fim and hora_fim > agendamento.hora_inicio):
                    raise ValidationError('Conflito de horário: O profissional já tem um agendamento neste horário.')


class HistoricoAtendimento(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='historico', verbose_name='Agendamento')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='historico_atendimentos', verbose_name='Pet')
    servico = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='historico_atendimentos', verbose_name='Serviço')
    profissional = models.ForeignKey(Profissional, on_delete=models.SET_NULL, null=True, blank=True, related_name='historico_atendimentos', verbose_name='Profissional')
    data_atendimento = models.DateTimeField('Data do Atendimento')
    valor_cobrado = models.DecimalField('Valor Cobrado', max_digits=10, decimal_places=2)
    observacoes = models.TextField('Observações', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Histórico de Atendimento'
        verbose_name_plural = 'Históricos de Atendimentos'
        ordering = ['-data_atendimento']

    def __str__(self):
        return f'{self.pet.nome} - {self.servico.name} - {self.data_atendimento}'
