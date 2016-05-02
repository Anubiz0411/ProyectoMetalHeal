#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from .models import UsuariosParaValidar
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget 
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form
from datetimewidget.widgets import DateWidget



class EditarForm(forms.Form):
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
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Correo electronico", required=True
    )
    photo = forms.ImageField(label="Foto", required=False)
    birthday = forms.DateField(widget = widgets.AdminDateWidget(), label="Fecha de nacimiento", required=True)


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )


class ValidateUserForm(forms.Form):

    elegido = forms.BooleanField()



class RegistrationUserForm(forms.Form):
    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'showMeridian' : True
    }
    cargo = (
        ('EP','EPS'),
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
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label="Foto",required=False)
    birthday  = forms.DateField(widget=DateWidget(attrs={'id':"yourdatetimeid"}, bootstrap_version=3, options=dateTimeOptions), label="Fecha de nacimiento", required=True)
    def clean_documento(self):
        usr = self.cleaned_data['documento']
        if User.objects.filter(username=usr):
            raise forms.ValidationError('Documento ya registrado.')
        return usr

    #def clean_email(self):
    #    email = self.cleaned_data['email']
    #    if User.objects.filter(email=email):
    #        raise forms.ValidationError('Ya existe un email igual en la base de datos')
    #    return email
    
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2= self.cleaned_data['password2']
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("La mínimo 8 caracteres, incluyendo una letra mayúscula y números.")
        if len(password) < 8:
            raise forms.ValidationError('La password debe tener al menos 8 caracteres.')
        if password!=password2:
            raise forms.ValidationError('Las passwords no coinciden')
        return password2

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

