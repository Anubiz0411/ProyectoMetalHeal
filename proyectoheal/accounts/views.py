# accounts/views.py
# coding=utf-8

from django.shortcuts import render, redirect

from django.core.urlresolvers import reverse
from django.core.mail import send_mail


from django.template import RequestContext
from proyectoheal.settings import EMAIL_HOST_USER

from django.contrib import admin, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegistrationUserForm,ResetPasswordForm,ValidateUserForm, EditarContrasenaForm, EditarForm, RecuperarUserForm, RegistrationEpsForm, EditarEmailForm

from .models import UsuariosParaValidar as UserProfile
from .models import *

from registration.backends.default.views import RegistrationView

#VISTA PARA  EDITAR CONTRASEÑA DESDE EL PANEL LOGUEADO
@login_required
def editar_password(request):
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
            messages.success(request, 'La password ha sido cambiado con exito!.')
            messages.success(request, 'Es necesario introducir los datos para entrar.')
            return redirect(reverse('accounts.index'))
    else:
        form = EditarContrasenaForm()
    usuario = UserProfile.objects.get(user__username=request.user.get_username())
    return render(request, 'accounts/editor_password.html', {'form': form,'usuario':usuario})

@login_required
def editar_email(request):
    if request.method == 'POST':
        form = EditarEmailForm(request.POST, request=request)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'El email ha sido cambiado con exito!.')
            return redirect(reverse('accounts.index'))
    else:
        form = EditarEmailForm(
            request=request,
            initial={'email': request.user.email})
    return render(request, 'accounts/editar_email.html', {'form': form})


@login_required
def editar_view(request,username):
    if request.method == 'POST':
        form = EditarForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            usuario = UserProfile.objects.get(user__username=username)
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            type_gen = cleaned_data.get('type_gen')
            type_doc = cleaned_data.get('type_doc')
            nombres = cleaned_data.get('nombres')
            apellidos = cleaned_data.get('apellidos')
            phone = cleaned_data.get('phone')
            direccion = cleaned_data.get('direccion')
            usuario.user.email = email
            usuario.photo = photo
            usuario.type_gen=type_gen
            usuario.type_doc=type_doc
            usuario.user.first_name=nombres
            usuario.user.last_name=apellidos
            usuario.phone=phone
            usuario.direccion=direccion
            usuario.user.save()
            usuario.save()
            return redirect(reverse('accounts.index'))
    else:
        form = EditarForm()
    usuario = UserProfile.objects.get(user__username=request.user.get_username())
    return render(request, 'accounts/editar.html', {'form': form,'usuario':usuario})

@login_required
def editar_usuario_view(request):
    if request.method == 'POST':
        form = EditarForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            usuario = UserProfile.objects.get(user__username=request.user.get_username())
            photo = cleaned_data.get('photo')
            nombres = cleaned_data.get('nombres')
            apellidos = cleaned_data.get('apellidos')
            phone = cleaned_data.get('phone')
            direccion = cleaned_data.get('direccion')
            usuario.photo = photo
            usuario.user.first_name=nombres
            usuario.user.last_name=apellidos
            usuario.phone=phone
            usuario.direccion=direccion
            usuario.user.save()
            usuario.save()
            messages.success(request, 'Se a modificado su perfil!.')
            return redirect(reverse('accounts.index'))
    else:
        form = EditarForm()
    usuario = UserProfile.objects.get(user__username=request.user.get_username())
    return render(request, 'accounts/editar.html', {'form': form,'usuario':usuario})

@login_required
def index_view(request):
    if request.user.is_superuser:
        return render(request, 'accounts/index.html')
    usr = request.user.get_username()
    usrs= UserProfile.objects.get(user__username=usr)
    return render(request, 'accounts/index.html',{'usuario':usrs})

@login_required
def validate(request):
    usr_name = request.user.get_username()
    usr4= UserProfile.objects.get(user__username=usr_name)
    if ( request.user.is_authenticated()   ):
        user = UserProfile.objects.get(user__username=usr_name)
        if user.type_user == 'SU':
            if request.method == 'POST':
                name = request.POST.get('usuario')
                texto,nombre = name.split("@")
                usr = UserProfile.objects.get(user__username=nombre)
                usr2 = User.objects.get(username=nombre)
                if texto=="validar":
                    usr.user.is_activate=True
                    usr2.is_active= True
                    email = usr.user.email
                    send_mail('Activacion Aprobada', 'La peticion de creacion de cuenta fue aprobada',
                              EMAIL_HOST_USER,
                              [email], fail_silently=False)
                    usr.save()
                    usr2.save()
                else:
                    usr.delete()
                    usr2.delete()
                    messages.success(request,'El usuario '+nombre+' fue eliminado con exito.')
            users_to_validate = UserProfile.objects.filter(user__is_active=False,type_user='EP')
            return render(request,'accounts/validate.html',{'to_validate':users_to_validate,'usuario':usr4})
        elif user.type_user == 'EP':
            if request.method == 'POST':
                name = request.POST.get('usuario')
                texto, nombre = name.split("@")
                usr = UserProfile.objects.get(user__username=nombre)
                usr2 = User.objects.get(username=nombre)
                if texto == "validar":
                    usr.user.is_activate = True
                    usr2.is_active = True
                    email = usr.user.email
                    send_mail('Activacion Aprobada', 'La peticion de creacion de cuenta fue aprobada',
                              EMAIL_HOST_USER,
                              [email], fail_silently=False)
                    usr.save()
                    usr2.save()
                else:
                    usr.delete()
                    usr2.delete()
                    messages.success(request, 'El usuario ' + nombre + ' fue eliminado con exito.')
            users_to_validate = UserProfile.objects.filter(user__is_active=False, type_user = 'PA' ) | UserProfile.objects.filter(user__is_active=False, type_user = 'ES' ) | UserProfile.objects.filter(user__is_active=False, type_user = 'GE' )
            return render(request, 'accounts/validate.html', {'to_validate': users_to_validate, 'usuario': usr4})
        else:
            return redirect(reverse('accounts.password_reset'))
    else:
        return redirect(reverse('accounts.password_reset'))

@login_required
def gestion_view(request):
        usr_name = request.user.get_username()
        usr4 = UserProfile.objects.get(user__username=usr_name)
        if (request.user.is_authenticated()):
            user = UserProfile.objects.get(user__username=usr_name)
            if user.type_user == 'SU':
                if request.method == 'POST':
                    name = request.POST.get('usuario')
                    texto, nombre = name.split("@")
                    usr = UserProfile.objects.get(user__username=nombre)
                    usr2 = User.objects.get(username=nombre)
                    if texto == "borrar":
                        usr.delete()
                        usr2.delete()
                        messages.success(request, 'El usuario ' + nombre + ' fue eliminado con exito.')
                    elif texto == "validar":
                        usr.user.is_activate = False
                        usr2.is_active = False
                        usr.save()
                        usr2.save()
                    else:
                        return redirect(reverse('accounts.editar', kwargs={'username': nombre}))
                users_to_validate = UserProfile.objects.filter(user__is_active=True, type_user='EP')
                return render(request, 'accounts/gestion_usuarios.html', {'to_validate': users_to_validate, 'usuario': usr4})
            elif user.type_user == 'EP':
                if request.method == 'POST':
                    name = request.POST.get('usuario')
                    texto, nombre = name.split("@")
                    usr = UserProfile.objects.get(user__username=nombre)
                    usr2 = User.objects.get(username=nombre)
                    if texto == "borrar":
                        usr.delete()
                        usr2.delete()
                        messages.success(request, 'El usuario ' + nombre + ' fue eliminado con exito.')
                    elif texto == "validar":
                        usr.user.is_activate = False
                        usr2.is_active = False
                        usr.save()
                        usr2.save()
                    else:
                        return redirect(reverse('accounts.editar', kwargs={'username': nombre}))
                users_to_validate = UserProfile.objects.filter(user__is_active=True,
                                                               type_user='PA') | UserProfile.objects.filter(
                    user__is_active=True, type_user='ES') | UserProfile.objects.filter(user__is_active=True,
                                                                                        type_user='GE')
                return render(request, 'accounts/gestion_usuarios.html', {'to_validate': users_to_validate, 'usuario': usr4})
            else:
                return redirect(reverse('accounts.password_reset'))
        else:
            return redirect(reverse('accounts.password_reset'))

@login_required
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
                              'mentalhealthdevteam@gmail.com',
                              [email], fail_silently=False)
            elif accion=="quitar":
                cita2 = Cita.objects.filter(IDmedico=request.user.get_username(),hora=str(int(horario)/7),fecha=str(int(horario)%7))
                email = usr.user.email
                usr_paciente = cita2[0].IDpaciente
                usuario_paciente = User.objects.get(username=usr_paciente)
                send_mail('Eliminacion de horario', 'La eliminacion de su horario fue exitoso.',
                          'mentalhealthdevteam@gmail.com',
                          [email], fail_silently=False)
                email2 = usuario_paciente.email
                send_mail('Eliminacion de horario', 'Lamentamos informarle que su cita fue cancelada.',
                          'mentalhealthdevteam@gmail.com',
                          [email2], fail_silently=False)
                cita2.delete()
            else:
                cita2 = Cita.objects.filter(IDmedico=request.user.get_username(), hora=str(int(horario) / 7),
                                            fecha=str(int(horario) % 7))
                email = usr.user.email
                send_mail('Eliminacion de horario', 'La eliminacion de su horario fue exitoso.',
                          'mentalhealthdevteam@gmail.com',
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
        return render(request, 'accounts/make_agenda.html', {'citas': list_final, 'usuario': usr})
    else:
        return redirect(reverse('accounts.index'))




@login_required
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
                              'mentalhealthdevteam@gmail.com',
                              [email], fail_silently=False)
                    id_medico = cita.IDmedico
                    medico = User.objects.get(username=id_medico)
                    email2 = medico.email
                    send_mail('Cita reservada', 'Existe una nueva cita agendada.',
                              'mentalhealthdevteam@gmail.com',
                              [email2], fail_silently=False)
            elif accion == "borrar":
                cita = Cita.objects.get(IDpaciente=username, hora=str(int(horario) / 7),
                                           fecha=str(int(horario) % 7))
                email = usr4.user.email
                send_mail('Eliminacion de horario', 'La eliminacion de su horario fue exitoso.',
                          'mentalhealthdevteam@gmail.com',
                          [email], fail_silently=False)
                id_medico = cita.IDmedico
                medico = User.objects.get(username=id_medico)
                email2 = medico.email
                send_mail('Eliminacion de horario', 'El paciente ha cancelado la cita.',
                          'mentalhealthdevteam@gmail.com',
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
        return render(request, 'accounts/make_agenda_paciente.html', {'citas': list_final, 'usuario': usr4})

    else:
        return redirect(reverse('accounts.index'))

@login_required
def mis_citas(request):
    username = request.user.get_username()
    usr4 = UserProfile.objects.get(user__username=username)
    tipo = usr4.type_user
    if tipo == 'GE':
        horario = Cita.objects.filter(IDpaciente = username).order_by('fecha','hora')

        return render(request, 'accounts/citas_paciente.html', {'citas': horario, 'usuario': usr4})
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
        return render(request, 'accounts/horario_medico.html', {'citas': horario, 'usuario': usr4})
    else:
        return redirect(reverse('accounts.index'))

def enviar_correo(email):
    send_mail('Activacion Pendiente', 'La peticion de creacion de cuenta esta en tramite',
              EMAIL_HOST_USER,
              [email], fail_silently=False)

#VISTA REGISTRO EPS
def registro_eps_view(request):
    if request.method == 'POST':
        form = RegistrationEpsForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('documento')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')

            type_user = cleaned_data.get('type_user')
            type_gen = cleaned_data.get('type_gen')
            type_doc = cleaned_data.get('type_doc')
            nombres = cleaned_data.get('cede')
            apellidos = cleaned_data.get('nombres')
            phone = cleaned_data.get('phone')
            direccion = cleaned_data.get('direccion')
            user_model = User.objects.create_user(username=username, password=password)
            user_model.email = email
            user_model.first_name = nombres
            user_model.last_name = apellidos
            user_model.is_active = False
            if type_user == 'SU':
                user_model.is_activate=True
            user_model.save()
            user_profile = UserProfile()
            user_profile.user = user_model
            user_profile.photo = photo
            user_profile.type_gen=type_gen
            user_profile.type_doc=type_doc
            user_profile.phone=phone
            user_profile.direccion = direccion
            user_profile.type_user=type_user
            user_profile.save()
            enviar_correo(email)
            return render(request, 'accounts/gracias.html', {'nombres': nombres})
    else:
        form = RegistrationEpsForm()
    context = {'form': form}
    return render(request, 'accounts/registro_eps.html', context)


def registro_usuario_view(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('documento')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            birthday = cleaned_data.get('birthday')
            type_user = cleaned_data.get('type_user')
            type_gen = cleaned_data.get('type_gen')
            type_doc = cleaned_data.get('type_doc')
            nombres = cleaned_data.get('nombres')
            apellidos = cleaned_data.get('apellidos')
            phone = cleaned_data.get('phone')
            direccion = cleaned_data.get('direccion')
            user_model = User.objects.create_user(username=username, password=password)
            user_model.email = email
            user_model.first_name = nombres
            user_model.last_name =apellidos
            user_model.is_active = False
            if type_user == 'SU':
                user_model.is_activate=True
            user_model.save()
            user_profile = UserProfile()
            user_profile.user = user_model
            user_profile.photo = photo
            user_profile.type_gen=type_gen
            user_profile.type_doc=type_doc
            user_profile.phone=phone
            user_profile.direccion = direccion
            user_profile.type_user=type_user
            user_profile.birthday=birthday
            user_profile.save()
            enviar_correo(email)
            return render(request, 'accounts/gracias.html', {'nombres': nombres})
    else:
        form = RegistrationUserForm()
    context = {'form': form}
    return render(request, 'accounts/registro_usuario.html', context)


def gracias_view(request, nombres):
    return render(request, 'accounts/gracias.html', {'nombres': nombres})


def login_view(request):
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        return redirect(reverse('accounts.index'))
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('accounts.index'))
            else:
                # Redireccionar informando que la cuenta esta inactiva
                # Lo dejo como ejercicio al lector :)
                pass
        mensaje = 'Nombre de usuario o contraseña no valido'
    return render(request, 'accounts/login.html', {'mensaje': mensaje})

def logout_view(request):
    logout(request)
    messages.success(request, 'Te has desconectado con exito.')
    return redirect(reverse('accounts.login'))

def recuperar_contrasena_view(request):
    if request.method == 'POST':
        # Si el method es post, obtenemos los datos del formulario
        form = RecuperarUserForm(request.POST, request.FILES)

        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el nombre del campo
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            email = cleaned_data.get('email')
            return render(request, 'accounts/recuperar_msj.html', {'email': email})
    else:
        # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
        form = RecuperarUserForm()
    # Creamos el contexto
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'accounts/recuperar.html', context)

def recuperar_msj_view(request, email):
    return render(request, 'accounts/recuperar_msj.html', {'email': email})

def registro_view(request):
    return render(request, 'accounts/registro.html')

