# agenda/urls.py

from django.conf.urls import include,url
from django.contrib.auth.forms import AdminPasswordChangeForm
from . import views
from django.contrib.auth.views import password_reset

urlpatterns = [
    # /agenda/
   	url(r'agenda/', views.crear_agenda,name='agenda.crear_agenda'),
    url(r'agenda_medico/', views.consultar_agenda, name='agenda.consultar_agenda'),
    url(r'agenda_paciente/', views.agendar_cita, name='agenda.agendar_cita'),
    url(r'consulta_paciente/', views.mis_citas, name='agenda.citas_paciente'),
]