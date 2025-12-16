from django.db import models
from django.contrib.auth.models import User
from servicos.models import Service


class Profissional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profissional', verbose_name='Usuário')
    nome = models.CharField('Nome', max_length=200)
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    especialidades = models.ManyToManyField(Service, related_name='profissionais', blank=True, verbose_name='Serviços que realiza')
    foto_url = models.CharField('URL da Foto', max_length=500, blank=True, null=True)
    cor_agenda = models.CharField('Cor na Agenda', max_length=7, default='#7C3AED')
    ativo = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class HorarioDisponivel(models.Model):
    DIA_SEMANA_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='horarios', verbose_name='Profissional')
    dia_semana = models.IntegerField('Dia da Semana', choices=DIA_SEMANA_CHOICES)
    hora_inicio = models.TimeField('Hora Início')
    hora_fim = models.TimeField('Hora Fim')
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Horário Disponível'
        verbose_name_plural = 'Horários Disponíveis'
        ordering = ['dia_semana', 'hora_inicio']
        unique_together = ['profissional', 'dia_semana', 'hora_inicio']

    def __str__(self):
        return f'{self.profissional.nome} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fim}'


class Folga(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='folgas', verbose_name='Profissional')
    data = models.DateField('Data')
    motivo = models.CharField('Motivo', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Folga'
        verbose_name_plural = 'Folgas'
        ordering = ['-data']

    def __str__(self):
        return f'{self.profissional.nome} - {self.data}'
