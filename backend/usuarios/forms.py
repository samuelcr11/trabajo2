from django import forms
from django.core.validators import EmailValidator


class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@dominio.com'}), validators=[EmailValidator()])
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': '********'}))


class RegisterForm(forms.Form):
    nombre = forms.CharField(label='Nombre completo', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre completo'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@dominio.com'}), validators=[EmailValidator()])
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': '********'}))
    rol = forms.ChoiceField(label='Rol', choices=[('usuario', 'Usuario'), ('administrador', 'Administrador')])


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@dominio.com'}), validators=[EmailValidator()])


class ProfileForm(forms.Form):
    nombre = forms.CharField(label='Nombre completo', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre completo'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'readonly': 'readonly'}))
    rol = forms.CharField(label='Rol', max_length=50, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha_registro = forms.CharField(label='Registrado desde', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
