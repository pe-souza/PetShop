import os
from datetime import datetime
from django.conf import settings
from twilio.rest import Client


class WhatsAppService:
    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
        self.whatsapp_from = os.environ.get('TWILIO_WHATSAPP_FROM', '')
        self.enabled = bool(self.account_sid and self.auth_token and self.whatsapp_from)
        
        if self.enabled:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
    
    def format_phone(self, phone):
        phone = ''.join(filter(str.isdigit, phone))
        if not phone.startswith('55'):
            phone = '55' + phone
        return f'whatsapp:+{phone}'
    
    def format_from_number(self):
        from_number = self.whatsapp_from
        if not from_number.startswith('whatsapp:'):
            if not from_number.startswith('+'):
                from_number = '+' + from_number
            from_number = f'whatsapp:{from_number}'
        return from_number
    
    def send_message(self, to_phone, message):
        if not self.enabled:
            return {'success': False, 'error': 'WhatsApp Twilio API não configurada'}
        
        try:
            twilio_message = self.client.messages.create(
                body=message,
                from_=self.format_from_number(),
                to=self.format_phone(to_phone)
            )
            
            return {
                'success': True, 
                'response': {
                    'sid': twilio_message.sid,
                    'status': twilio_message.status
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def format_message(self, template, agendamento):
        replacements = {
            '{cliente_nome}': agendamento.cliente.nome,
            '{pet_nome}': agendamento.pet.nome,
            '{servico_nome}': agendamento.servico.name,
            '{data}': agendamento.data.strftime('%d/%m/%Y'),
            '{hora}': agendamento.hora_inicio.strftime('%H:%M'),
            '{profissional_nome}': agendamento.profissional.nome if agendamento.profissional else 'Equipe',
            '{preco}': f'R$ {agendamento.preco:.2f}',
        }
        
        message = template
        for key, value in replacements.items():
            message = message.replace(key, str(value))
        
        return message


def enviar_confirmacao_agendamento(agendamento):
    from .models import MensagemTemplate, MensagemEnviada
    
    service = WhatsAppService()
    
    try:
        template = MensagemTemplate.objects.get(tipo='confirmacao', ativo=True)
        mensagem = service.format_message(template.template, agendamento)
    except MensagemTemplate.DoesNotExist:
        mensagem = f"""Ola {agendamento.cliente.nome}!

Seu agendamento foi confirmado:

Data: {agendamento.data.strftime('%d/%m/%Y')}
Horario: {agendamento.hora_inicio.strftime('%H:%M')}
Pet: {agendamento.pet.nome}
Servico: {agendamento.servico.name}
Valor: R$ {agendamento.preco:.2f}

Pet Shop Amigo - Cuidando do seu pet com amor!"""
        template = None
    
    resultado = service.send_message(agendamento.cliente.telefone, mensagem)
    
    registro = MensagemEnviada.objects.create(
        agendamento=agendamento,
        template=template,
        telefone=agendamento.cliente.telefone,
        mensagem=mensagem,
        status='enviada' if resultado['success'] else 'erro',
        erro_mensagem=resultado.get('error'),
        enviada_em=datetime.now() if resultado['success'] else None
    )
    
    if resultado['success']:
        agendamento.whatsapp_confirmacao_enviada = True
        agendamento.save()
    
    return resultado


def enviar_lembrete_agendamento(agendamento):
    from .models import MensagemTemplate, MensagemEnviada
    
    service = WhatsAppService()
    
    try:
        template = MensagemTemplate.objects.get(tipo='lembrete', ativo=True)
        mensagem = service.format_message(template.template, agendamento)
    except MensagemTemplate.DoesNotExist:
        mensagem = f"""Ola {agendamento.cliente.nome}!

Lembrete: Seu agendamento e AMANHA!

Data: {agendamento.data.strftime('%d/%m/%Y')}
Horario: {agendamento.hora_inicio.strftime('%H:%M')}
Pet: {agendamento.pet.nome}
Servico: {agendamento.servico.name}

Esperamos voce!
Pet Shop Amigo"""
        template = None
    
    resultado = service.send_message(agendamento.cliente.telefone, mensagem)
    
    registro = MensagemEnviada.objects.create(
        agendamento=agendamento,
        template=template,
        telefone=agendamento.cliente.telefone,
        mensagem=mensagem,
        status='enviada' if resultado['success'] else 'erro',
        erro_mensagem=resultado.get('error'),
        enviada_em=datetime.now() if resultado['success'] else None
    )
    
    if resultado['success']:
        agendamento.whatsapp_lembrete_enviado = True
        agendamento.save()
    
    return resultado


def enviar_cancelamento(agendamento):
    from .models import MensagemTemplate, MensagemEnviada
    
    service = WhatsAppService()
    
    try:
        template = MensagemTemplate.objects.get(tipo='cancelamento', ativo=True)
        mensagem = service.format_message(template.template, agendamento)
    except MensagemTemplate.DoesNotExist:
        mensagem = f"""Ola {agendamento.cliente.nome},

Seu agendamento foi cancelado:

Data: {agendamento.data.strftime('%d/%m/%Y')}
Horario: {agendamento.hora_inicio.strftime('%H:%M')}
Pet: {agendamento.pet.nome}
Servico: {agendamento.servico.name}

Para reagendar, entre em contato conosco.

Pet Shop Amigo"""
        template = None
    
    resultado = service.send_message(agendamento.cliente.telefone, mensagem)
    
    MensagemEnviada.objects.create(
        agendamento=agendamento,
        template=template,
        telefone=agendamento.cliente.telefone,
        mensagem=mensagem,
        status='enviada' if resultado['success'] else 'erro',
        erro_mensagem=resultado.get('error'),
        enviada_em=datetime.now() if resultado['success'] else None
    )
    
    return resultado
