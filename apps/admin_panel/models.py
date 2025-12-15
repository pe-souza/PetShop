from django.db import models
from django.contrib.auth.models import User
from apps.services.models import Service

class Testimonial(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Reprovado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário', null=True, blank=True)
    author_name = models.CharField('Nome do autor', max_length=100)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Serviço avaliado')
    rating = models.IntegerField('Nota', choices=[(i, str(i)) for i in range(1, 6)], default=5)
    comment = models.TextField('Comentário')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Depoimento'
        verbose_name_plural = 'Depoimentos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.rating} estrelas'
