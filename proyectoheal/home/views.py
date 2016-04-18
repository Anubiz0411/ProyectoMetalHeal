# home/views.py
 # coding=utf-8
from proyectoheal.settings import EMAIL_HOST_USER
from django.shortcuts import render
from django.utils import timezone
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from .forms import ContactUsuarioAnonimoForm, ContactUsuarioLoginForm
from django.views import generic

# Creamos una función para el envió de email
# (es muy simple, solo para demostrar como enviar un email)
def send_email_contact(email_usuario, subject, body):
    body = '{} ha enviado un email de contacto\n\n{}\n\n{}'.format(email_usuario, subject, body)
    send_mail(
        subject='Nuevo email de contacto',
        message=body,
        from_email=email_usuario,
        recipient_list=[EMAIL_HOST_USER]
    )

class ContactView(generic.FormView):

    template_name = 'home/contact.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.form_class = ContactUsuarioLoginForm
        else:
            self.form_class = ContactUsuarioAnonimoForm
        return super(ContactView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')
        body = form.cleaned_data.get('body')
        if self.request.user.is_authenticated():
            email_usuario = self.request.user.email
            send_email_contact(email_usuario, subject, body)
        else:
            email_usuario = form.cleaned_data.get('email')
            send_email_contact(email_usuario, subject, body)
        messages.success(self.request, 'Email enviado con exito')
        return super(ContactView, self).form_valid(form)

def index_view(request):
    return render(request, 'home/index.html')

def AboutView(request):
    return render(request, 'home/about.html')