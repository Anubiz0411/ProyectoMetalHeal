from django.contrib import admin
from models import UsuariosParaValidar
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail

def validar(modeladmin, request, queryset):
    for q in queryset:
        q.user.is_active = True
        send_mail('Activacion Aprobada', 'La peticion de creacion de cuenta fue aprobada',
                  'mentalhealthdevteam@gmail.com',
                  [q.user.email], fail_silently=False)
        q.user.save()

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['user','type_user','photo']
    actions = [validar]


admin.site.register(UsuariosParaValidar,UserModelAdmin)
admin.site.unregister(Group)