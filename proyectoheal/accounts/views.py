# accounts/views.py
# coding=utf-8

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse

from .forms import RegistroEps, RegistroEspecialistaForm, RegistroUserForm, RecuperarUserForm, EditarEmailForm, EditarContrasenaForm, EditarPerfilForm
from .models import *

from django.template import RequestContext
from django.core.mail import send_mail
from proyectoheal.settings import EMAIL_HOST_USER




@login_required
def index_view(request):
    return render(request, 'accounts/index.html')

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

def registro_view(request):
    return render(request, 'accounts/registro.html')

def registro_eps_view(request):
    if request.method == 'POST':

        form = RegistroEps(request.POST, request.FILES)

        if form.is_valid():

            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            phone = cleaned_data.get('phone')
            email = cleaned_data.get('email')

            user_model = User.objects.create_user(username=username, password=password)

            user_model.first_name = first_name
            user_model.save()
            user_model.last_name = last_name
            user_model.save()
            user_model.phone = phone
            user_model.save()
            user_model.email = email

            user_model.save()

            user_profile = EpsProfile()
            # Al campo user le asignamos el objeto user_model
            user_profile.user = user_model
            html_content = 'Su cuenta se encuentra esta en Inactiva, Espere a que el Administrador le autorize el ingeso.'
            send_mail(first_name, html_content, EMAIL_HOST_USER, [email], fail_silently=False)
            # y le asignamos la photo (el campo, permite datos null)
 
            user_profile.save()

            return render(request, 'accounts/gracias.html', {'first_name': first_name})
    else:
        # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
        form = RegistroEps()
    # Creamos el contexto
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'accounts/registro_eps.html', context)

def registro_especialista_view(request):
    if request.method == 'POST':
        # Si el method es post, obtenemos los datos del formulario
        form = RegistroEspecialistaForm(request.POST, request.FILES)
        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el nombre del campo
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            especialista = cleaned_data.get('especialista')
            phone = cleaned_data.get('phone')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            # E instanciamos un objeto User, con el username y password
            user_model = User.objects.create_user(username=username, password=password)
            # Añadimos el email
            user_model.first_name = first_name
            user_model.save()
            user_model.last_name = last_name
            user_model.save()
            user_model.especialista = especialista
            user_model.save()
            user_model.phone = phone
            user_model.save()
            user_model.email = email
            # Y guardamos el objeto, esto guardara los datos en la db.
            user_model.save()
            # Ahora, creamos un objeto UserProfile, aunque no haya incluido
            # una imagen, ya quedara la referencia creada en la db.
            user_profile = EspecialistaProfile()
            # Al campo user le asignamos el objeto user_model
            user_profile.user = user_model
            # y le asignamos la photo (el campo, permite datos null)
            user_profile.photo = photo
            # Por ultimo, guardamos tambien el objeto UserProfile
            user_profile.save()
            html_content = 'Su cuenta se encuentra esta en Inactiva, Espere a que su EPS le autorize el ingeso, o comunuquese con el Administrador de su EPS.'
            send_mail(first_name, html_content, EMAIL_HOST_USER, [email], fail_silently=False)
            # Ahora, redireccionamos a la pagina accounts/gracias.html
            # Pero lo hacemos con un redirect.
            return render(request, 'accounts/gracias.html', {'first_name': first_name})
    else:
        # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
        form = RegistroEspecialistaForm()
    # Creamos el contexto
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'accounts/registro_especialista.html', context)

def registro_medico_view(request):
    if request.method == 'POST':
        # Si el method es post, obtenemos los datos del formulario
        form = RegistroUserForm(request.POST, request.FILES)
        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el nombre del campo
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            phone = cleaned_data.get('phone')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            # E instanciamos un objeto User, con el username y password
            user_model = User.objects.create_user(username=username, password=password)
            # Añadimos el email
            user_model.first_name = first_name
            user_model.save()
            user_model.last_name = last_name
            user_model.save()
            user_model.phone = phone
            user_model.save()
            user_model.email = email
            # Y guardamos el objeto, esto guardara los datos en la db.
            user_model.save()
            # Ahora, creamos un objeto MedicalProfile, aunque no haya incluido
            # una imagen, ya quedara la referencia creada en la db.
            user_profile = MedicalProfile()
            # Al campo user le asignamos el objeto user_model
            user_profile.user = user_model
            # y le asignamos la photo (el campo, permite datos null)
            user_profile.photo = photo
            # Por ultimo, guardamos tambien el objeto MedicalProfile
            user_profile.save()
            html_content = 'Su cuenta se encuentra esta en Inactiva, Espere a que su EPS le autorize el ingeso, o comunuquese con el Administrador de su EPS.'
            send_mail(first_name, html_content, EMAIL_HOST_USER, [email], fail_silently=False)
            # Ahora, redireccionamos a la pagina accounts/gracias.html
            # Pero lo hacemos con un redirect.
            return render(request, 'accounts/gracias.html', {'first_name': first_name})
    else:
        # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
        form = RegistroUserForm()
    # Creamos el contexto
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'accounts/registro_usuario.html', context)

def registro_usuario_view(request):
    if request.method == 'POST':
        # Si el method es post, obtenemos los datos del formulario
        form = RegistroUserForm(request.POST, request.FILES)
        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el nombre del campo
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            phone = cleaned_data.get('phone')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            # E instanciamos un objeto User, con el username y password
            user_model = User.objects.create_user(username=username, password=password)
            # Añadimos el email
            user_model.first_name = first_name
            user_model.save()
            user_model.last_name = last_name
            user_model.save()
            user_model.phone = phone
            user_model.save()
            user_model.email = email
            # Y guardamos el objeto, esto guardara los datos en la db.
            user_model.save()
            # Ahora, creamos un objeto PatientProfile, aunque no haya incluido
            # una imagen, ya quedara la referencia creada en la db.
            user_profile = PatientProfile()
            # Al campo user le asignamos el objeto user_model
            user_profile.user = user_model
            # y le asignamos la photo (el campo, permite datos null)
            user_profile.photo = photo
            # Por ultimo, guardamos tambien el objeto PatientProfile
            user_profile.save()
            html_content = 'Su cuenta se encuentra esta en Inactiva, Espere a que su EPS le autorize el ingeso, o comunuquese con el Administrador de su EPS.'
            send_mail(first_name, html_content, EMAIL_HOST_USER, [email], fail_silently=False)
            # Ahora, redireccionamos a la pagina accounts/gracias.html
            # Pero lo hacemos con un redirect.
            return render(request, 'accounts/gracias.html', {'first_name': first_name})
    else:
        # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
        form = RegistroUserForm()
    # Creamos el contexto
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'accounts/registro_usuario.html', context)

def gracias_view(request, first_name):
    return render(request, 'accounts/gracias.html', {'first_name': first_name})

def recuperar_contrasena_view(request):
    if request.method == 'POST':
        # Si el method es post, obtenemos los datos del formulario
        form = RecuperarUserForm(request.POST, request.FILES)

        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el nombre del cam                           po
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            return redirect(reverse('accounts.gracias'))
    else:
        # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
        form = RecuperarUserForm()
    # Creamos el contexto
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'accounts/recuperar.html', context)

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
def editar_contrasena(request):
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
            messages.success(request, 'La contraseña ha sido cambiado con exito!.')
            messages.success(request, 'Es necesario introducir los datos para entrar.')
            return redirect(reverse('accounts.index'))
    else:
        form = EditarContrasenaForm()
    return render(request, 'accounts/editar_contrasena.html', {'form': form})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.phone = form.cleaned_data['phone']
            request.user.save()
            messages.success(request, 'Se a modificado su perfil!.')
            return redirect(reverse('accounts.index'))
    else:
        form = EditarPerfilForm()
    return render(request, 'accounts/editar_perfil.html', {'form': form})

