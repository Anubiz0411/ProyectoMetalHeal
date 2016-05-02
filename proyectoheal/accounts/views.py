from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import admin



from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationUserForm,ResetPasswordForm,ValidateUserForm,RegistrationScheduleForm
from .models import UsuariosParaValidar as UserProfile


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from registration.backends.default.views import RegistrationView
from django.contrib.auth.hashers import make_password

# Modificar al inicio
from .forms import  RegistrationUserForm, EditarContrasenaForm, EditarForm

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
def crear_agenda(request):
    if request.method == 'POST':
        form = RegistrationScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            hora = cleaned_data.get('hora')
            fecha = cleaned_data.get('fecha')
            cita = Cita()
            cita.hora = hora
            cita.fecha=fecha
            cita.IDpaciente= '-1'
            cita.save()
            return redirect(reverse('accounts.index'))
        else:
            form = RegistrationScheduleForm()
    context = {'form': form}
    return render(request, 'accounts/registro.html', context)



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
        form = EditarForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            usuario = UserProfile.objects.get(user__username=request.user.get_username())
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

def enviar_correo(email):
    send_mail('Activacion Pendiente', 'La peticion de creacion de cuenta esta en tramite',
              'mentalhealthdevteam@gmail.com',
              [email], fail_silently=False)




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
            return redirect(reverse('accounts.gracias', kwargs={'username': username}))
    else:
        form = RegistrationUserForm()
    context = {'form': form}
    return render(request, 'accounts/registro.html', context)


def gracias_view(request, username):
    return render(request, 'accounts/gracias.html', {'username': username})



@login_required
def index_view(request):
    if request.user.is_superuser:
        return redirect(reverse('accounts.password_reset'))
    usr = request.user.get_username()
    usrs= UserProfile.objects.get(user__username=usr)
    return render(request, 'accounts/index.html',{'usuario':usrs})

def login_view(request):
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        return render(reverse('accounts.index'))
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
                return render(request,'accounts/validacion_pendiente.html',{'username': username})
        mensaje = 'Nombre de usuario o passwords no valido'
    return render(request, 'accounts/login.html', {'mensaje': mensaje})

def logout_view(request):
    logout(request)
    messages.success(request, 'Te has desconectado con exito.')
    return redirect(reverse('accounts.login'))

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
                              'mentalhealthdevteam@gmail.com',
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
                              'mentalhealthdevteam@gmail.com',
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


