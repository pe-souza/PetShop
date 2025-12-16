from django.db import models
from clientes.models import Cliente


class Pet(models.Model):
    ESPECIE_CHOICES = [
        ('cachorro', 'Cachorro'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('roedor', 'Roedor'),
        ('reptil', 'Réptil'),
        ('outro', 'Outro'),
    ]
    
    PORTE_CHOICES = [
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pets', verbose_name='Dono')
    nome = models.CharField('Nome', max_length=100)
    especie = models.CharField('Espécie', max_length=20, choices=ESPECIE_CHOICES, default='cachorro')
    raca = models.CharField('Raça', max_length=100, blank=True, null=True)
    porte = models.CharField('Porte', max_length=20, choices=PORTE_CHOICES, blank=True, null=True)
    data_nascimento = models.DateField('Data de nascimento', blank=True, null=True)
    peso = models.DecimalField('Peso (kg)', max_digits=5, decimal_places=2, blank=True, null=True)
    cor = models.CharField('Cor/Pelagem', max_length=100, blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    alergias = models.TextField('Alergias', blank=True, null=True)
    ativo = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.cliente.nome})'
    
    @property
    def idade(self):
        if self.data_nascimento:
            from datetime import date
            today = date.today()
            anos = today.year - self.data_nascimento.year
            if today.month < self.data_nascimento.month or (today.month == self.data_nascimento.month and today.day < self.data_nascimento.day):
                anos -= 1
            return anos
        return None
