from django import forms
from django.core.exceptions import ValidationError
from datetime import date


class ReservationForm(forms.Form):
    recurso_id = forms.CharField(label='Recurso ID', widget=forms.TextInput(attrs={'placeholder': 'ID del recurso'}))
    fecha = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'type': 'date'}))
    hora_inicio = forms.TimeField(label='Hora inicio', widget=forms.TimeInput(attrs={'type': 'time'}))
    hora_fin = forms.TimeField(label='Hora fin', widget=forms.TimeInput(attrs={'type': 'time'}))

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < date.today():
            raise ValidationError('La fecha debe ser futura.')
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('hora_inicio')
        fin = cleaned_data.get('hora_fin')
        fecha = cleaned_data.get('fecha')
        if inicio and fin and inicio >= fin:
            raise ValidationError('La hora de fin debe ser posterior a la de inicio.')
        if inicio and fin and (fin.hour - inicio.hour) > 12:
            raise ValidationError('La reserva no puede durar más de 12 horas.')
        if fecha and fecha < date.today():
            raise ValidationError('La reserva debe programarse para una fecha posterior o igual a hoy.')
        return cleaned_data
