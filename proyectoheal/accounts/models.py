# accounts.models.py

from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    username = models.CharField(max_length=254,unique=False)
    first_name = models.CharField(max_length=254, unique=False)
    last_name = models.CharField(max_length=254, unique=False)
    phone = models.CharField(max_length=254, unique=False)
    email = models.EmailField(max_length=254, unique=False)

    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
            

class EpsProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=True)
    is_eps = models.BooleanField(default=True)
    username = models.CharField(max_length=254,unique=False)
    first_name = models.CharField(max_length=254, unique=False)
    last_name = models.CharField(max_length=254, unique=False)
    phone = models.CharField(max_length=254, unique=False)
    email = models.EmailField(max_length=254, unique=False)

    class Meta:
        verbose_name = 'EPS'
        verbose_name_plural = 'EPSs'


class EspecialistaProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=True)
    is_especialista = models.BooleanField(default=True)
    username = models.CharField(max_length=254,unique=False)
    first_name = models.CharField(max_length=254, unique=False)
    last_name = models.CharField(max_length=254, unique=False)
    especialidad = models.CharField(max_length=254, unique=False)
    phone = models.CharField(max_length=254, unique=False)
    email = models.EmailField(max_length=254, unique=False)
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)

    class Meta:
        verbose_name = 'Especialista'
        verbose_name_plural = 'Especialistas'

class MedicalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=True)
    is_medical = models.BooleanField(default=True)
    username = models.CharField(max_length=254,unique=False)
    first_name = models.CharField(max_length=254, unique=False)
    last_name = models.CharField(max_length=254, unique=False)
    phone = models.CharField(max_length=254, unique=False)
    email = models.EmailField(max_length=254, unique=False)
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)

    class Meta:
        verbose_name = 'Medico'
        verbose_name_plural = 'Medicos'

class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=True)
    is_patient = models.BooleanField(default=True)
    username = models.CharField(max_length=254,unique=False)
    first_name = models.CharField(max_length=254, unique=False)
    last_name = models.CharField(max_length=254, unique=False)
    phone = models.CharField(max_length=254, unique=False)
    email = models.EmailField(max_length=254, unique=False)
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

            


