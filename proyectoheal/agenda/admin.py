from django.contrib import admin
from models import Cita
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail

admin.site.register(Cita)
