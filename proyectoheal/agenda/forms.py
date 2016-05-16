# agenda/forms.py
# coding=utf-8
#!/usr/bin/env python

from proyectoheal.settings import EMAIL_HOST_USER

from django.core.mail import send_mail
from django.core.validators import RegexValidator

from django.template.context_processors import *

from django import forms

from registration.forms import RegistrationForm



from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget 
from django.contrib.admin import widgets

from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form

from datetimewidget.widgets import DateWidget,TimeWidget


#FORMULARIO DE REGISTRO CITAS
class RegistrationScheduleForm(forms.Form):
    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'showMeridian' : True
    }
    hora =forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
    fecha=forms.DateField(widget=DateWidget(attrs={'id':"yourdatetimeid"}, bootstrap_version=3, options=dateTimeOptions), label="Fecha", required=True) 