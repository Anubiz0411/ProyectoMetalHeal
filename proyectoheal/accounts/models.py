from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime

class Cita(models.Model):
    IDmedico=models.CharField(max_length=20)
    hora=models.CharField(max_length=10)
    fecha=models.CharField(max_length=10)
    disponible = models.BooleanField(default=False)
    IDpaciente = models.CharField(max_length=20, default="-1")
    
class UsuariosParaValidar(models.Model):
    cargo = (
        ('EP','EPS'),
        ('SU','ADMINISTRADOR'),
        ('PA', 'Paciente'),
        ('GE', 'Medico General'),
        ('ES', 'Medico Especialista'),
    )
    doc=(
        ('CC','CEDULA DE CIUDADANIA'),
        ('CE','CEDULA DE EXTRANGERIA'),
        ('NI','NIT'),
        ('PA','PASAPORTE'),
    )
    genero=(
        ('H','HOMBRE'),
        ('M','MUJER'),
        ('O','OTRO'),
    )
    birthday = models.DateField(default="1980-04-28")
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    type_user = models.CharField(max_length=2, choices=cargo, default='PA')
    photo = models.ImageField(upload_to='profiles', blank=True,null=True)
    REQUIRED_FIELDS = ['user','type_user']
    direccion = models.CharField(max_length=40,default='villa x cs 10')
    phone = models.CharField(max_length=10,default='3333333')
    type_doc = models.CharField(max_length=2,choices=doc,default='CC')
    type_gen = models.CharField(max_length=1, choices=genero, default='H')
    def __str__(self):
        return self.user.username
    def get_short_name(self):
        return str(self.type_user)
    def get_full_name(self):
        return str(self.photo)


