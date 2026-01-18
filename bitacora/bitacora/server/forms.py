from django import forms
from .models import *
import requests
from django.core.exceptions import ValidationError
import re
from django.forms.widgets import DateInput, TimeInput

class BitacoraAccesoForm(forms.ModelForm): 
    nombre_visitante = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'nombre_visitante', 
            'placeholder': 'Buscar visitante...'
        })
    )
    fecha = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #9ca3af;'}))
    hora_entrada = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'class': 'form-control', 'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #9ca3af;'}))
    hora_salida = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'class': 'form-control', 'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #9ca3af;'}))
    
    class Meta: 
        model = BitacoraAcceso
        fields = ['fecha', 'hora_entrada', 'hora_salida', 'nombre_visitante', 'ubicacion', 'motivo_visita', 'responsable', 'observaciones', 'rut', 'apellido_paterno', 'apellido_materno',  'ticket']
        widgets = {
            'motivo_visita': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el motivo de la visita (requerido)',  
                    'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #9ca3af; height: 70px;',
                    'required': 'required' 
                }
            ),
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido paterno del visitante',
                'readonly': 'readonly'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido materno del visitante',
                'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #9ca3af;',
                'readonly': 'readonly'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el RUT del visitante',
                'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #9ca3af;',
                'readonly': 'readonly'
            }),

            'ticket': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese observaciones (opcional)', 'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #9ca3af; height: 70px;'})
        }
    

class LoginForm(forms.Form):
    usuario = forms.CharField(
        max_length=150,
        label='Usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}),
        label='Contraseña'
    )



class BitacoraAccesoExternaForm(forms.ModelForm):
    
    class Meta:
        model = BitacoraAcceso
        fields = ['fecha', 'hora_entrada', 'hora_salida', 'nombre_visitante', 'ubicacion', 'motivo_visita', 
                  'responsable', 'observaciones',  'ticket','externo']
        widgets = {
            'nombre_visitante': forms.TextInput(attrs={'placeholder': 'Ingresar Nombre del Visitante','required': 'required' }),

            'fecha': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Seleccione la fecha'}),  # Added placeholder
            'hora_entrada': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Hora de entrada'}),  # Added placeholder
            'hora_salida': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Hora de salida'}),  # Added placeholder
            'motivo_visita': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el motivo de la visita (requerido)',  
                    'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #9ca3af;',
                    'required': 'required' 
                }
            ),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Agregue observaciones si las hay'}),  # Added placeholder
            'ticket': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'externo': forms.HiddenInput()  # Oculta el campo en el HTML

        }

    def clean_nombre_visitante(self):
        nombre = self.cleaned_data.get('nombre_visitante')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise ValidationError('Solo se permiten letras y espacios en el nombre del visitante.')
        return nombre
