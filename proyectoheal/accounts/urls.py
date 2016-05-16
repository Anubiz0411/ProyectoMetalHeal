from django.conf.urls import include,url
from django.contrib.auth.forms import AdminPasswordChangeForm
from . import views
from django.contrib.auth.views import password_reset

urlpatterns = [
    url(r'^$', views.index_view, name='accounts.index'),
    url(r'^validate/$',views.validate,name='accounts.validate'),
    url(r'^login/$', views.login_view, name='accounts.login'),
    url(r'^logout/$',views.logout_view,name="accounts.logout"),

    url(r'^registro/$',views.registro_view, name = 'accounts.registro'),
    url(r'^registro/registro_eps/$', views.registro_eps_view, name='accounts.registro_eps'),
    url(r'^registro/registro_especialista/$', views.registro_usuario_view, name='accounts.registro_usuario'),
    url(r'^registro/registro_usuario/$', views.registro_usuario_view, name='accounts.registro_usuario'),
    url(r'gracias/(?P<username>[\w]+)/$', views.gracias_view,name='accounts.gracias'),

    url(r'^recuperar/$', views.recuperar_contrasena_view, name='accounts.recuperar'),
    url(r'^recuperar_msj$', views.recuperar_msj_view, name='accounts.recuperar_msj'),

     url(r'agenda/', views.crear_agenda,name='accounts.crear_agenda'),
    url(r'agenda_medico/', views.consultar_agenda, name='accounts.consultar_agenda'),
    url(r'agenda_paciente/', views.agendar_cita, name='accounts.agendar_cita'),
    url(r'consulta_paciente/', views.mis_citas, name='accounts.citas_paciente'),

    url(r'editar/(?P<username>[\w]+)/$', views.editar_view,name='accounts.editar'),
    url(r'editar_usr/$', views.editar_usuario_view,name='accounts.editar_usuario'),
    url(r'^editar_email/$', views.editar_email, name='accounts.editar_email'),
    url(r'^editar_password/$', views.editar_password, name='accounts.editar_password'),
    

    url(r'^gestion_usuario/$', views.gestion_view, name='accounts.gestion_usuario'),
    url(r'^password_change/$',  # hijack password_change's url
        'django.contrib.auth.views.password_change',
        {'password_change_form': AdminPasswordChangeForm},
        name="accounts.password_change"),
    url(r'^password_reset/$', password_reset,{'html_email_template_name':
             'accounts/password_reset.html'},
        name='accounts.password_reset',
        ),
    url(r'^accounts/', include('django.contrib.auth.urls')),

]

