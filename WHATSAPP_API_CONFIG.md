# Configuração da API do WhatsApp - Pet Shop Amigo

## Visão Geral

O sistema Pet Shop Amigo possui integração com WhatsApp para envio automático de:
- **Confirmação de agendamento** - Enviada quando um agendamento é criado
- **Lembrete** - Enviado antes do horário agendado
- **Cancelamento** - Enviado quando um agendamento é cancelado
- **Reagendamento** - Enviado quando há alteração de data/hora

---

## Opções de API

### Opção 1: WhatsApp Cloud API (Meta/Facebook)

A API oficial do WhatsApp, gerenciada pela Meta.

#### Passo a passo:

1. **Criar conta de desenvolvedor**
   - Acesse: https://developers.facebook.com/
   - Crie uma conta ou faça login

2. **Criar aplicativo**
   - Vá em "Meus Aplicativos" > "Criar Aplicativo"
   - Selecione "Empresa" ou "Outro"
   - Escolha "WhatsApp" nos produtos

3. **Configurar WhatsApp Business**
   - Configure um número de telefone comercial
   - Verifique o número (você receberá um código SMS)

4. **Obter credenciais**
   - **WHATSAPP_API_URL**: `https://graph.facebook.com/v17.0`
   - **WHATSAPP_PHONE_NUMBER_ID**: ID do seu número (encontrado no painel)
   - **WHATSAPP_API_TOKEN**: Token de acesso permanente

5. **Configurar Templates de Mensagem**
   - Vá em WhatsApp > Gerenciador de Modelos
   - Crie templates para: confirmação, lembrete, cancelamento
   - Aguarde aprovação (pode levar 24-48h)

---

### Opção 2: Twilio

Plataforma de comunicação com API simples.

#### Passo a passo:

1. **Criar conta**
   - Acesse: https://www.twilio.com/
   - Crie uma conta (inclui créditos grátis para teste)

2. **Ativar WhatsApp Sandbox (para testes)**
   - No Console, vá em Messaging > Try it out > WhatsApp
   - Envie a mensagem de ativação para o número indicado

3. **Obter credenciais**
   - **TWILIO_ACCOUNT_SID**: Encontrado no Dashboard
   - **TWILIO_AUTH_TOKEN**: Encontrado no Dashboard
   - **TWILIO_WHATSAPP_FROM**: Número WhatsApp Twilio

4. **Para produção**
   - Solicite um número WhatsApp Business
   - Complete a verificação da empresa

---

## Configuração no Sistema

### Variáveis de Ambiente

Configure as seguintes variáveis de ambiente no Replit (aba Secrets):

```
WHATSAPP_API_URL=https://graph.facebook.com/v17.0
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id
WHATSAPP_API_TOKEN=seu_token_de_acesso
```

Ou para Twilio:
```
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_WHATSAPP_FROM=+14155238886
```

---

## Templates de Mensagem

### Variáveis Disponíveis

Use estas variáveis nos templates de mensagem:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{cliente_nome}` | Nome do cliente | Maria Silva |
| `{pet_nome}` | Nome do pet | Rex |
| `{servico_nome}` | Nome do serviço | Banho e Tosa |
| `{data}` | Data do agendamento | 25/12/2025 |
| `{hora}` | Horário | 14:30 |
| `{profissional_nome}` | Nome do profissional | João |
| `{preco}` | Valor do serviço | R$ 85,00 |

### Exemplos de Templates

#### Confirmação de Agendamento
```
Olá {cliente_nome}! 🐾

Seu agendamento foi confirmado:

📅 Data: {data}
⏰ Horário: {hora}
🐕 Pet: {pet_nome}
✂️ Serviço: {servico_nome}
👨‍⚕️ Profissional: {profissional_nome}
💰 Valor: {preco}

Pet Shop Amigo - Cuidando do seu pet com amor! 💜
```

#### Lembrete (1 dia antes)
```
Olá {cliente_nome}! 🐾

Lembrete: Seu agendamento é AMANHÃ!

📅 Data: {data}
⏰ Horário: {hora}
🐕 Pet: {pet_nome}
✂️ Serviço: {servico_nome}

Esperamos você! 💜
Pet Shop Amigo
```

#### Cancelamento
```
Olá {cliente_nome},

Seu agendamento foi cancelado:

📅 Data: {data}
⏰ Horário: {hora}
🐕 Pet: {pet_nome}

Para reagendar, entre em contato conosco.

Pet Shop Amigo 💜
```

---

## Configurando no Painel Administrativo

1. Acesse `/admin-panel/` e faça login
2. Vá em **WhatsApp** no menu lateral
3. Cadastre seus templates personalizados
4. Ative/desative cada tipo de mensagem

---

## Testando a Integração

### Teste Manual

1. Crie um agendamento de teste
2. Verifique se a mensagem foi enviada no histórico (WhatsApp > Mensagens Enviadas)
3. Confirme o recebimento no WhatsApp do cliente

### Verificar Logs

Os logs de envio ficam salvos na tabela `MensagemEnviada`:
- Status: Pendente, Enviada, Entregue, Lida, Erro
- Mensagem de erro (se houver)
- Data/hora do envio

---

## Limitações e Custos

### WhatsApp Cloud API (Meta)
- **Grátis**: 1.000 conversas/mês (iniciadas pelo negócio)
- **Custo adicional**: ~$0.005 a $0.08 por mensagem (varia por país)

### Twilio
- **Sandbox**: Grátis para testes
- **Produção**: ~$0.005 por mensagem + custo do número

---

## Suporte

Em caso de dúvidas sobre a configuração:
1. Verifique os logs de erro no painel administrativo
2. Confirme se as variáveis de ambiente estão corretas
3. Teste a API diretamente usando Postman ou curl

---

## Segurança

⚠️ **Importante:**
- Nunca compartilhe suas credenciais de API
- Use variáveis de ambiente para armazenar tokens
- Revogue tokens comprometidos imediatamente
- Em produção, use HTTPS sempre
