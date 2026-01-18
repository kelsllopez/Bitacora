from django import forms
from .models import BitacoraInterna, BitacoraExterna

class BitacoraInternaForm(forms.ModelForm):
    class Meta:
        model = BitacoraInterna
        fields = ['fecha', 'hora_entrada', 'hora_salida', 'modo_visita', 
                  'nombre_visitante', 'apellido_paterno', 'apellido_materno', 
                  'rut', 'ticket', 'responsable', 'ubicacion', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'modo_visita':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese el motivo de la visita '}),
            'nombre_visitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'ticket': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }

class BitacoraExternaForm(forms.ModelForm):
    class Meta:
        model = BitacoraExterna
        fields = ['fecha', 'hora_entrada', 'hora_salida', 'modo_visita', 
                  'nombre_visitante', 'ticket', 'responsable', 'ubicacion', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'modo_visita':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese el motivo de la visita '}),
            'nombre_visitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Visitante'}),
            'ticket': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }