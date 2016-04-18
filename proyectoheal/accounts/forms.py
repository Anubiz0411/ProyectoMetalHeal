# accounts/forms.py
 # coding=utf-8
from proyectoheal.settings import EMAIL_HOST_USER
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.template.context_processors import *

#FORMULARIO PARA REGISTRAR EPS
class RegistroEps(forms.Form):
    
    username= forms.CharField(
        label='Nit.',
        min_length=8,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(
        label='Razon Socila',
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(
        label='Nombre de la Persona de Contacto',
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone = forms.CharField(
        label='Telefono Contacto',
        min_length=7,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    email = forms.EmailField(
        label='Correo Electronico Contacto',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Contraseña',
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir Contraseña',
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

        
    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la base de datos.')
        return email

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2


#FORMULARIO PARA REGISTRAR DE MEDICO ESPECIALISTA
class RegistroEspecialistaForm(forms.Form):
 
    username= forms.CharField(
        label='Cedula',
        min_length=8,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(
        label='Nombres',
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(
        label='Apellidos',
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    especialidad = forms.CharField(
        label='Especialidad',
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone = forms.CharField(
        label='Telefono',
        min_length=7,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    email = forms.EmailField(
        label='Correo Electronico',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Contraseña',
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir Contraseña',
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    photo = forms.ImageField(label='Foto', required=False)
        

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la base de datos.')
        return email

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

#FORMULARIO PARA REGISTRAR USUARIO
class RegistroUserForm(forms.Form):
    
    username= forms.CharField(
        label='Cedula',
        min_length=8,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(
        label='Nombres',
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(
        label='Apellidos',
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone = forms.CharField(
        label='Telefono',
        min_length=7,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    email = forms.EmailField(
        label='Correo Electronico',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Contraseña',
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir Contraseña',
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    photo = forms.ImageField(label='Foto', required=False)
        
    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la base de datos.')
        return email

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

#FORMULARIO PARA RECUPERAR LA CONTRASEÑA
class RecuperarUserForm(forms.Form):
    
    username = forms.CharField(
        label='Usuario',
        min_length=8,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(
            label='Correo',
            min_length=8,
            widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            pass
        else:
            raise forms.ValidationError('El usuario no esta Registrado')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            send_mail('Cambio de Contraseña', 
            'Para cambiar su contraseña dirijase al siguiente enlace', 
            EMAIL_HOST_USER, 
            [email], 
            fail_silently=False)
            pass
        else:
            raise forms.ValidationError('Este correo no corresponde a su usuario.')
        return email

    
#FORMULARIO PARA CAMBIAR CORREO
class EditarEmailForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Obtener request"""
        self.request = kwargs.pop('request')
        return super(EditarEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Comprobar si ha cambiado el email
        actual_email = self.request.user.email
        username = self.request.user.username
        if email != actual_email:
            # Si lo ha cambiado, comprobar que no exista en la db.
            # Exluye el usuario actual.
            existe = User.objects.filter(email=email).exclude(username=username)
            if existe:
                raise forms.ValidationError('Ya existe un email igual en la db.')
        return email

#FORMULARIO PARA CAMBIAR CONTRASEÑA
class EditarContrasenaForm(forms.Form):

    actual_password = forms.CharField(
        label='Contraseña actual',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Nueva contraseña',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir contraseña',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

#FORMULARIO PARA CAMBIAR PERFIL
class EditarPerfilForm(forms.Form):

    first_name = forms.CharField(
        label='Nombres',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(
        label='Apellidos',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone = forms.CharField(
        label='Telefono',
        widget=forms.TextInput(attrs={'class': 'form-control'}))


