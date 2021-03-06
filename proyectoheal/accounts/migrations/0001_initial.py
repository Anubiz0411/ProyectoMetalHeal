# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-16 07:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDmedico', models.CharField(max_length=20)),
                ('hora', models.CharField(max_length=10)),
                ('fecha', models.CharField(max_length=10)),
                ('disponible', models.BooleanField(default=False)),
                ('IDpaciente', models.CharField(default='-1', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UsuariosParaValidar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(default='1980-04-28')),
                ('type_user', models.CharField(choices=[('EP', 'EPS'), ('SU', 'ADMINISTRADOR'), ('PA', 'Paciente'), ('GE', 'Medico General'), ('ES', 'Medico Especialista')], default='PA', max_length=2)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profiles')),
                ('direccion', models.CharField(default='villa x cs 10', max_length=40)),
                ('phone', models.CharField(default='3333333', max_length=10)),
                ('type_doc', models.CharField(choices=[('CC', 'CEDULA DE CIUDADANIA'), ('CE', 'CEDULA DE EXTRANGERIA'), ('NI', 'NIT'), ('PA', 'PASAPORTE')], default='CC', max_length=2)),
                ('type_gen', models.CharField(choices=[('H', 'HOMBRE'), ('M', 'MUJER'), ('O', 'OTRO')], default='H', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
