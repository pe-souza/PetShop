from django.db import models


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', blank=True, null=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Service(models.Model):
    PORTE_CHOICES = [
        ('todos', 'Todos os portes'),
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
    ]
    
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicos', verbose_name='Categoria')
    name = models.CharField('Nome', max_length=200)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    preco_porte_medio = models.DecimalField('Preço Porte Médio', max_digits=10, decimal_places=2, blank=True, null=True)
    preco_porte_grande = models.DecimalField('Preço Porte Grande', max_digits=10, decimal_places=2, blank=True, null=True)
    duracao_minutos = models.PositiveIntegerField('Duração (minutos)', default=30)
    porte_aplicavel = models.CharField('Porte Aplicável', max_length=20, choices=PORTE_CHOICES, default='todos')
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def get_preco_por_porte(self, porte):
        if porte == 'medio' and self.preco_porte_medio:
            return self.preco_porte_medio
        elif porte == 'grande' and self.preco_porte_grande:
            return self.preco_porte_grande
        return self.price
