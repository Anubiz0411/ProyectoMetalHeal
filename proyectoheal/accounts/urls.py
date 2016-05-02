from django.conf.urls import include,url
from django.contrib.auth.forms import AdminPasswordChangeForm
from . import views
from django.contrib.auth.views import password_reset

urlpatterns = [
    url(r'^$', views.index_view, name='accounts.index'),
    url(r'^validate/$',views.validate,name='accounts.validate'),
    url(r'^login/$', views.login_view, name='accounts.login'),
    url(r'^logout/$',views.logout_view,name="accounts.logout"),
    url(r'^registro/$',views.registro_usuario_view, name = 'accounts.registro'),
    url(r'gracias/(?P<username>[\w]+)/$', views.gracias_view,name='accounts.gracias'),
    url(r'editar/(?P<username>[\w]+)/$', views.editar_view,name='accounts.editar'),
    url(r'editar_usr/$', views.editar_usuario_view,name='accounts.editar_usuario'),
    url(r'^editar_password/$', views.editar_password, name='accounts.editar_password'),
    url(r'agenda/(?P<username>[\w]+)/$', views.crear_agenda,name='accounts.crear_agenda'),
    url(r'^gestion_usuario/$', views.gestion_view, name='accounts.gestion_usuario'),
    url(r'^password_change/$',  # hijack password_change's url
        'django.contrib.auth.views.password_change',
        {'password_change_form': AdminPasswordChangeForm},
        name="accounts.password_change"),
    url(r'^password_reset/$',
        password_reset,
        {'html_email_template_name':
             'accounts/password_reset.html'},
        name='accounts.password_reset',
        ),
    url(r'^accounts/', include('django.contrib.auth.urls')),

]

