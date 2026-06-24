from django import forms
from django.core.exceptions import ValidationError
from datetime import date, datetime, time
from .services import list_reservations


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
        recurso_id = cleaned_data.get('recurso_id')
        
        # Validar orden de horas
        if inicio and fin and inicio >= fin:
            raise ValidationError('La hora de fin debe ser posterior a la de inicio.')
        
        # Validar duración máxima
        if inicio and fin and (fin.hour - inicio.hour) > 12:
            raise ValidationError('La reserva no puede durar más de 12 horas.')
        
        # Validar fecha no sea pasada
        if fecha and fecha < date.today():
            raise ValidationError('La reserva debe programarse para una fecha posterior o igual a hoy.')
        
        # Validar conflictos de horario con reservas existentes
        if fecha and inicio and fin and recurso_id:
            try:
                fecha_str = fecha.isoformat()
                inicio_str = inicio.isoformat(timespec='minutes')
                fin_str = fin.isoformat(timespec='minutes')
                
                reservas_existentes = list_reservations(fecha=fecha_str)
                for reserva in reservas_existentes:
                    if reserva.get('recurso_id') == recurso_id and reserva.get('estado') != 'cancelada':
                        hora_inicio_existente = reserva.get('hora_inicio', '')[:5]
                        hora_fin_existente = reserva.get('hora_fin', '')[:5]
                        inicio_str_short = inicio_str[:5]
                        fin_str_short = fin_str[:5]
                        
                        # Verificar conflicto
                        if not (fin_str_short <= hora_inicio_existente or inicio_str_short >= hora_fin_existente):
                            raise ValidationError(
                                f'El recurso ya está reservado en ese horario. '
                                f'Conflicto con reserva de {hora_inicio_existente} a {hora_fin_existente}.'
                            )
            except ValidationError:
                raise
            except Exception:
                # Si hay error en la validación de conflictos, continuar (puede ser fallo de Firebase)
                pass
        
        return cleaned_data

