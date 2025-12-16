from django.db import models
from agendamentos.models import Agendamento


class MensagemTemplate(models.Model):
    TIPO_CHOICES = [
        ('confirmacao', 'Confirmação de Agendamento'),
        ('lembrete', 'Lembrete'),
        ('cancelamento', 'Cancelamento'),
        ('reagendamento', 'Reagendamento'),
        ('pos_atendimento', 'Pós-atendimento'),
    ]
    
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, unique=True)
    template = models.TextField('Template da Mensagem')
    ativo = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Template de Mensagem'
        verbose_name_plural = 'Templates de Mensagens'

    def __str__(self):
        return self.get_tipo_display()


class MensagemEnviada(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('enviada', 'Enviada'),
        ('entregue', 'Entregue'),
        ('lida', 'Lida'),
        ('erro', 'Erro'),
    ]
    
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='mensagens_whatsapp', verbose_name='Agendamento')
    template = models.ForeignKey(MensagemTemplate, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Template')
    telefone = models.CharField('Telefone', max_length=20)
    mensagem = models.TextField('Mensagem')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    erro_mensagem = models.TextField('Mensagem de Erro', blank=True, null=True)
    enviada_em = models.DateTimeField('Enviada em', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem Enviada'
        verbose_name_plural = 'Mensagens Enviadas'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.telefone} - {self.get_status_display()}'
