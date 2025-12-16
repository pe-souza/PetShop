from datetime import datetime


class WhatsAppService:
    def __init__(self):
        self.enabled = False
    
    def format_phone(self, phone):
        phone = ''.join(filter(str.isdigit, phone))
        if not phone.startswith('55'):
            phone = '55' + phone
        return phone
    
    def send_message(self, to_phone, message):
        return {'success': False, 'error': 'WhatsApp API não configurada'}
    
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
    pass


def enviar_lembrete_agendamento(agendamento):
    pass


def enviar_cancelamento(agendamento):
    pass
