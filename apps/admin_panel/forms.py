from django import forms
from apps.services.models import Service
from .models import Testimonial

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do serviço'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Descrição do serviço'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': '0.00'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
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
