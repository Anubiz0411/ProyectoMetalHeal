# agenda/views.py
# coding=utf-8

from django.shortcuts import render, redirect

from django.core.urlresolvers import reverse
from django.core.mail import send_mail


from django.template import RequestContext
from proyectoheal.settings import EMAIL_HOST_USER

from django.contrib import admin, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationScheduleForm
from .models import Cita
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import admin

from accounts.models import UsuariosParaValidar as UserProfile

@login_required
def mis_citas(request):
    username = request.user.get_username()
    usr4 = UserProfile.objects.get(user__username=username)
    tipo = usr4.type_user
    if tipo == 'GE':
        horario = Cita.objects.filter(IDpaciente = username).order_by('fecha','hora')

        return render(request, 'agenda/citas_paciente.html', {'citas': horario, 'usuario': usr4})
    else:
        return redirect(reverse('accounts.index'))

@login_required
def consultar_agenda(request):
    username = request.user.get_username()
    usr4 = UserProfile.objects.get(user__username=username)
    tipo = usr4.type_user
    messages.success(request, tipo)
    if tipo == 'GE' or tipo == 'ES':
        horario = Cita.objects.filter(IDmedico=username,disponible=True).order_by('fecha','hora')
        return render(request, 'agenda/horario_medico.html', {'citas': horario, 'usuario': usr4})
    else:
        return redirect(reverse('accounts.index'))

def crear_agenda(request):
    hor = Cita.objects.all()
    username = request.user.get_username()
    usr = UserProfile.objects.get(user__username=username)
    tipo = usr.type_user
    if tipo == 'GE' or tipo == 'ES':
        if request.method == 'POST':
            texto = request.POST.get('usuario')
            accion,horario = texto.split('@')
            if accion == "activar":
                cita_aux = Cita.objects.filter(IDmedico=request.user.get_username(),hora=str(int(horario)/7),fecha=str(int(horario)%7))
                if len(cita_aux) > 0 :
                    messages.success(request,'Este horario ya esta registrado.')
                else:
                    cita = Cita()
                    cita.hora = str(int(horario)/7)
                    cita.fecha = str(int(horario)%7)
                    cita.IDmedico= request.user.get_username()
                    cita.disponible=True
                    cita.save()
                    email = usr.user.email
                    send_mail('Activacion de horario', 'El registro de su horario fue exitoso.',
                              EMAIL_HOST_USER,
                              [email], fail_silently=False)
            elif accion=="quitar":
                cita2 = Cita.objects.filter(IDmedico=request.user.get_username(),hora=str(int(horario)/7),fecha=str(int(horario)%7))
                email = usr.user.email
                usr_paciente = cita2[0].IDpaciente
                usuario_paciente = User.objects.get(username=usr_paciente)
                send_mail('Eliminacion de horario', 'La eliminacion de su horario fue exitoso.',
                          EMAIL_HOST_USER,
                          [email], fail_silently=False)
                email2 = usuario_paciente.email
                send_mail('Eliminacion de horario', 'Lamentamos informarle que su cita fue cancelada.',
                          EMAIL_HOST_USER,
                          [email2], fail_silently=False)
                cita2.delete()
            else:
                cita2 = Cita.objects.filter(IDmedico=request.user.get_username(), hora=str(int(horario) / 7),
                                            fecha=str(int(horario) % 7))
                email = usr.user.email
                send_mail('Eliminacion de horario', 'La eliminacion de su horario fue exitoso.',
                          EMAIL_HOST_USER,
                          [email], fail_silently=False)
                cita2.delete()

        list = []
        list2 = []
        for i in range(0,175):
            hora = i / 7
            fecha = i % 7
            cita = Cita.objects.filter(hora = hora, fecha = fecha, IDmedico = username)
            esta_activo = False
            esta_pedido = False
            if len(cita) > 0:
                    for j in cita:
                        if j.disponible :
                            esta_activo =True
                            break
                        if j.IDpaciente != "-1":
                            esta_pedido = True
            if esta_activo:
                list.append(1)
            elif esta_pedido:
                list.append(2)
            else:
                list.append(0)
            list2.append(i)
        list_final = zip(list,list2)
        return render(request, 'agenda/make_agenda.html', {'citas': list_final, 'usuario': usr})
    else:
        return redirect(reverse('accounts.index'))

def agendar_cita(request):
    username = request.user.get_username()
    usr4 = UserProfile.objects.get(user__username=username)
    tipo = usr4.type_user
    if tipo == 'PA':
        if request.method == 'POST':
            texto = request.POST.get('usuario')
            accion, horario = texto.split('@')
            if accion == "activar":
                cita_aux = Cita.objects.filter(hora=str(int(horario) / 7),
                                               fecha=str(int(horario) % 7))
                if len(cita_aux) <= 0:
                    messages.success(request, 'Este horario no esta disponible.')
                else:
                    cita = cita_aux[0]
                    cita.IDpaciente = username
                    cita.disponible=False
                    cita.save()
                    email = usr4.user.email
                    send_mail('Activacion de horario', 'El registro de su horario fue exitoso.',
                              EMAIL_HOST_USER,
                              [email], fail_silently=False)
                    id_medico = cita.IDmedico
                    medico = User.objects.get(username=id_medico)
                    email2 = medico.email
                    send_mail('Cita reservada', 'Existe una nueva cita agendada.',
                              EMAIL_HOST_USER,
                              [email2], fail_silently=False)
            elif accion == "borrar":
                cita = Cita.objects.get(IDpaciente=username, hora=str(int(horario) / 7),
                                           fecha=str(int(horario) % 7))
                email = usr4.user.email
                send_mail('Eliminacion de horario', 'La eliminacion de su horario fue exitoso.',
                          EMAIL_HOST_USER,
                          [email], fail_silently=False)
                id_medico = cita.IDmedico
                medico = User.objects.get(username=id_medico)
                email2 = medico.email
                send_mail('Eliminacion de horario', 'El paciente ha cancelado la cita.',
                          EMAIL_HOST_USER,
                          [email2], fail_silently=False)
                cita.IDpaciente = "-1"
                cita.disponible=True
                cita.save()
            else:
                messages.success(request,'Esta cita no se puede agendar.')

        list = []
        list2 = []
        for i in range(0, 175):
            hora = i / 7
            fecha = i % 7
            cita = Cita.objects.filter(hora=hora, fecha=fecha)
            if len(cita) > 0:
                puso = False
                for j in cita:
                    if j.IDpaciente == username:
                        list.append(1)
                        puso = True
                        break
                if not puso:
                    list.append(0)
            else:
                list.append(2)
            list2.append(i)
        list_final = zip(list, list2)
        return render(request, 'agenda/make_agenda_paciente.html', {'citas': list_final, 'usuario': usr4})

    else:
        return redirect(reverse('accounts.index'))

