from django.db import models


class Cliente(models.Model):
    nome = models.CharField('Nome completo', max_length=200)
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail', blank=True, null=True)
    cpf = models.CharField('CPF', max_length=14, blank=True, null=True)
    endereco = models.CharField('Endereço', max_length=300, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=100, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    ativo = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome
    
    def telefone_whatsapp(self):
        telefone = ''.join(filter(str.isdigit, self.telefone))
        if not telefone.startswith('55'):
            telefone = '55' + telefone
        return telefone
