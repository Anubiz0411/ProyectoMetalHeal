from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime



class Cita(models.Model):
    hora=models.TimeField(auto_now=False)
    fecha=models.DateField(default=False)
    IDmedico=models.CharField(max_length=20)
    disponible = models.BooleanField(default=False)
    IDpaciente = models.CharField(max_length=20, default="-1")

