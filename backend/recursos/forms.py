from django import forms

TIPOS = [
    ('sala', 'Sala'),
    ('laboratorio', 'Laboratorio'),
    ('equipo', 'Equipo'),
    ('proyector', 'Proyector'),
]
ESTADOS = [
    ('disponible', 'Disponible'),
    ('mantenimiento', 'Mantenimiento'),
    ('ocupado', 'Ocupado'),
]


class ResourceForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Nombre del recurso'}))
    descripcion = forms.CharField(label='Descripción', widget=forms.Textarea(attrs={'placeholder': 'Detalle del recurso', 'rows': 3}))
    tipo = forms.ChoiceField(label='Tipo', choices=TIPOS)
    imagen = forms.URLField(label='URL imagen', required=False, widget=forms.URLInput(attrs={'placeholder': 'https://...' }))
    estado = forms.ChoiceField(label='Estado', choices=ESTADOS)
