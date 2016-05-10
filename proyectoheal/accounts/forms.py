# accounts/forms.py
# coding=utf-8
#!/usr/bin/env python

from proyectoheal.settings import EMAIL_HOST_USER

from django.core.mail import send_mail
from django.core.validators import RegexValidator

from django.template.context_processors import *

from django import forms

from registration.forms import RegistrationForm

from .models import UsuariosParaValidar

from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget 
from django.contrib.admin import widgets

from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form

from datetimewidget.widgets import DateWidget,TimeWidget


class EditarForm(forms.Form):

    nombres = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombres", required=True
    )
    apellidos = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Apellidos", required=True
    )
    phone = forms.CharField(
        min_length=7,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Telefono", required=True
    )
    direccion = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Direccion", required=True
    )
    
    birthday = forms.DateField(widget = widgets.AdminDateWidget(), label="Fecha de nacimiento", required=True)

    photo = forms.ImageField(label="Foto", required=False)


    def clean_phone(self):
        phn = self.cleaned_data['phone']
        if not phn.isdigit():
            raise forms.ValidationError('Solo puede contener números')
        if len(phn) != 7 and len(phn) != 10:
            raise forms.ValidationError('Telefono inválido.')
        return phn

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class ValidateUserForm(forms.Form):
    elegido = forms.BooleanField()
    
#FORMULARIO DE REGISTRO CITAS
class RegistrationScheduleForm(forms.Form):
    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'showMeridian' : True
    }
    hora =forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
    fecha=forms.DateField(widget=DateWidget(attrs={'id':"yourdatetimeid"}, bootstrap_version=3, options=dateTimeOptions), label="Fecha de nacimiento", required=True) 

#FORMULARIO DE REGISTRO USUARIOS
class RegistrationUserForm(forms.Form):
    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'showMeridian' : True
    }
    cargo = (
        ('PA', 'Paciente'),
        ('GE', 'Medico General'),
        ('ES', 'Medico Especialista'),
    )
    doc = (
        ('CC', 'CEDULA DE CIUDADANIA'),
        ('CE', 'CEDULA DE EXTRANGERIA'),
        ('NI', 'NIT'),
        ('PA', 'PASAPORTE'),
    )
    genero = (
        ('H', 'HOMBRE'),
        ('M', 'MUJER'),
        ('O', 'OTRO'),
    )
    type_user = forms.ChoiceField(
        label="Cargo",
        required=True,
        choices=cargo)

    type_gen = forms.ChoiceField(
        label="Genero",
        required=True,
        choices=genero
    )
    type_doc = forms.ChoiceField(
        label="Documento",
        required=True,
        choices=doc
    )
    documento = forms.CharField(
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Documento", required=True
    )

    nombres = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombres", required=True
    )
    apellidos = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Apellidos",required=True
    )
    phone = forms.CharField(
        min_length=7,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Telefono", required=True
    )
    direccion = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Direccion", required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Correo electronico", required=True
    )

    password = forms.CharField(
        min_length=8,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        min_length=8,
        label="Repetir Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    photo = forms.ImageField(label="Foto",required=False)

    birthday = forms.DateField(widget = widgets.AdminDateWidget(), label="Fecha de nacimiento", required=True)

    def __init__(self, *args, **kwargs):
        super(RegistrationUserForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget = widgets.AdminDateWidget()
    
    def clean_documento(self):
        usr = self.cleaned_data['documento']
        if User.objects.filter(username=usr):
            raise forms.ValidationError('Documento ya registrado.')
        return usr

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la base de datos')
        return email
    def clean_phone(self):
        phn = self.cleaned_data['phone']
        if not phn.isdigit():
            raise forms.ValidationError('Solo puede contener números')
        if len(phn) != 7 and len(phn) != 10:
            raise forms.ValidationError('Telefono inválido.')
        return phn
    
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2= self.cleaned_data['password2']
        first_isalpha = password[0].isalpha()
        if password == password.lower():
            raise forms.ValidationError('La password debe contener al menos una letra en mayúscula.')
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("La password debe contener mínimo 8 caracteres, incluyendo una letra mayúscula y números.")
        if len(password) < 8:
            raise forms.ValidationError('La password debe tener al menos 8 caracteres.')
        if password!=password2:
            raise forms.ValidationError('Las passwords no coinciden')
        return password2

#FORMULARIO DE REGISTRO EPS
class RegistrationEpsForm(forms.Form):
    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'showMeridian' : True
    }
    cargo = (
        ('EP','EPS'),
    )
    doc = (
        ('NI', 'NIT'),
    )
    genero = (
        ('O', 'OTRO'),
    )
    type_user = forms.ChoiceField(
        label="Cargo",
        required=True,
        choices=cargo)

    type_gen = forms.ChoiceField(
        label="Genero",
        required=True,
        choices=genero
    )
    type_doc = forms.ChoiceField(
        label="Tipo de Documento",
        required=True,
        choices=doc
    )

    documento = forms.CharField(
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Numero de Identificacion", required=True
    )

    cede = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombre EPS", required=True
    )

    phone = forms.CharField(
        min_length=7,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Telefono", required=True
    )
    direccion = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Direccion", required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Correo electronico", required=True
    )
    nombre = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombre Persona de Contacto",required=True
    )
    
    password = forms.CharField(
        min_length=8,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        min_length=8,
        label="Repetir Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    photo = forms.ImageField(label="Foto",required=False)

    
    def clean_documento(self):
        usr = self.cleaned_data['documento']
        if User.objects.filter(username=usr):
            raise forms.ValidationError('Documento ya registrado.')
        return usr

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la base de datos')
        return email

    def clean_phone(self):
        phn = self.cleaned_data['phone']
        if not phn.isdigit():
            raise forms.ValidationError('Solo puede contener números')
        if len(phn) != 7 and len(phn) != 10:
            raise forms.ValidationError('Telefono inválido.')
        return phn
    
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2= self.cleaned_data['password2']
        first_isalpha = password[0].isalpha()
        if password == password.lower():
            raise forms.ValidationError('La password debe contener al menos una letra en mayúscula.')
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("La password debe contener mínimo 8 caracteres, incluyendo una letra mayúscula y números.")
        if len(password) < 8:
            raise forms.ValidationError('La password debe tener al menos 8 caracteres.')
        if password!=password2:
            raise forms.ValidationError('Las passwords no coinciden')
        return password2

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
        first_isalpha = password[0].isalpha()
        if password == password.lower():
            raise forms.ValidationError('La password debe contener al menos una letra en mayúscula.')
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("La password debe contener mínimo 8 caracteres, incluyendo una letra mayúscula y números.")
        if len(password) < 8:
            raise forms.ValidationError('La password debe tener al menos 8 caracteres.')
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

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

