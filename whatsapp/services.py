import os
import requests
from datetime import datetime
from django.conf import settings


class WhatsAppService:
    def __init__(self):
        self.api_url = os.environ.get('WHATSAPP_API_URL', '')
        self.api_token = os.environ.get('WHATSAPP_API_TOKEN', '')
        self.phone_number_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')
        self.enabled = bool(self.api_url and self.api_token)
    
    def format_phone(self, phone):
        phone = ''.join(filter(str.isdigit, phone))
        if not phone.startswith('55'):
            phone = '55' + phone
        return phone
    
    def send_message(self, to_phone, message):
        if not self.enabled:
            return {'success': False, 'error': 'WhatsApp API não configurada'}
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'messaging_product': 'whatsapp',
                'to': self.format_phone(to_phone),
                'type': 'text',
                'text': {'body': message}
            }
            
            response = requests.post(
                f'{self.api_url}/{self.phone_number_id}/messages',
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return {'success': True, 'response': response.json()}
            else:
                return {'success': False, 'error': response.text}
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
        mensagem = f"""Olá {agendamento.cliente.nome}! 🐾

Seu agendamento foi confirmado:

📅 Data: {agendamento.data.strftime('%d/%m/%Y')}
⏰ Horário: {agendamento.hora_inicio.strftime('%H:%M')}
🐕 Pet: {agendamento.pet.nome}
✂️ Serviço: {agendamento.servico.name}
💰 Valor: R$ {agendamento.preco:.2f}

Pet Shop Amigo - Cuidando do seu pet com amor! 💜"""
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
        mensagem = f"""Olá {agendamento.cliente.nome}! 🐾

Lembrete: Seu agendamento é AMANHÃ!

📅 Data: {agendamento.data.strftime('%d/%m/%Y')}
⏰ Horário: {agendamento.hora_inicio.strftime('%H:%M')}
🐕 Pet: {agendamento.pet.nome}
✂️ Serviço: {agendamento.servico.name}

Esperamos você! 💜
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
        mensagem = f"""Olá {agendamento.cliente.nome},

Seu agendamento foi cancelado:

📅 Data: {agendamento.data.strftime('%d/%m/%Y')}
⏰ Horário: {agendamento.hora_inicio.strftime('%H:%M')}
🐕 Pet: {agendamento.pet.nome}
✂️ Serviço: {agendamento.servico.name}

Para reagendar, entre em contato conosco.

Pet Shop Amigo 💜"""
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
