from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.about, name='about'),
    path('contato/', views.contact, name='contact'),
    path('agendar/', views.agendar_online, name='agendar_online'),
    path('agendar/horarios/', views.get_horarios_disponiveis, name='get_horarios'),
    path('agendar/criar/', views.criar_agendamento_online, name='criar_agendamento'),
    path('agendar/sucesso/', views.agendar_sucesso, name='agendar_sucesso'),
]
