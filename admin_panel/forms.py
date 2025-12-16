from django import forms
from django.contrib.auth.models import User
from servicos.models import Service, Categoria
from clientes.models import Cliente
from pets.models import Pet
from profissionais.models import Profissional, HorarioDisponivel, Folga
from agendamentos.models import Agendamento
from whatsapp.models import MensagemTemplate
from .models import Testimonial


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['categoria', 'name', 'description', 'price', 'preco_porte_medio', 'preco_porte_grande', 'duracao_minutos', 'porte_aplicavel', 'is_active']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do serviço'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Descrição do serviço'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Preço base'}),
            'preco_porte_medio': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Preço porte médio'}),
            'preco_porte_grande': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Preço porte grande'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Duração em minutos'}),
            'porte_aplicavel': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome da categoria'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'cpf', 'endereco', 'bairro', 'cidade', 'observacoes', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome completo'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@exemplo.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '000.000.000-00'}),
            'endereco': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Rua, número'}),
            'bairro': forms.TextInput(attrs={'class': 'form-input'}),
            'cidade': forms.TextInput(attrs={'class': 'form-input'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['cliente', 'nome', 'especie', 'raca', 'porte', 'data_nascimento', 'peso', 'cor', 'observacoes', 'alergias', 'ativo']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-input'}),
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do pet'}),
            'especie': forms.Select(attrs={'class': 'form-input'}),
            'raca': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Raça'}),
            'porte': forms.Select(attrs={'class': 'form-input'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'peso': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Peso em kg'}),
            'cor': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Cor/Pelagem'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'alergias': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Alergias conhecidas'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class ProfissionalForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome de usuário para login'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Senha'}))
    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}), label='Administrador')
    
    class Meta:
        model = Profissional
        fields = ['nome', 'telefone', 'especialidades', 'cor_agenda', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do profissional'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(00) 00000-0000'}),
            'especialidades': forms.SelectMultiple(attrs={'class': 'form-input', 'size': '5'}),
            'cor_agenda': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class HorarioDisponivelForm(forms.ModelForm):
    class Meta:
        model = HorarioDisponivel
        fields = ['dia_semana', 'hora_inicio', 'hora_fim', 'ativo']
        widgets = {
            'dia_semana': forms.Select(attrs={'class': 'form-input'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class FolgaForm(forms.ModelForm):
    class Meta:
        model = Folga
        fields = ['data', 'motivo']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'motivo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Motivo da folga'}),
        }


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'pet', 'servico', 'profissional', 'data', 'hora_inicio', 'preco', 'status', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-input'}),
            'pet': forms.Select(attrs={'class': 'form-input'}),
            'servico': forms.Select(attrs={'class': 'form-input'}),
            'profissional': forms.Select(attrs={'class': 'form-input'}),
            'data': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'preco': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.none()
        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['pet'].queryset = Pet.objects.filter(cliente_id=cliente_id, ativo=True)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['pet'].queryset = self.instance.cliente.pets.filter(ativo=True)


class MensagemTemplateForm(forms.ModelForm):
    class Meta:
        model = MensagemTemplate
        fields = ['tipo', 'template', 'ativo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-input'}),
            'template': forms.Textarea(attrs={'class': 'form-input', 'rows': 6, 'placeholder': 'Use {cliente_nome}, {pet_nome}, {servico_nome}, {data}, {hora}, {profissional_nome}, {preco}'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['author_name', 'service', 'rating', 'comment', 'status']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-input'}),
            'service': forms.Select(attrs={'class': 'form-input'}),
            'rating': forms.Select(attrs={'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }
