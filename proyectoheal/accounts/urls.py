# accounts/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='accounts.index'),
    url(r'^login/$', views.login_view, name='accounts.login'),
    url(r'^logout/$', views.logout_view, name='accounts.logout'),
    
    url(r'^recuperar/$', views.recuperar_contrasena_view, name='accounts.recuperar'),
    url(r'^recuperar_msj$', views.recuperar_msj_view, name='accounts.recuperar_msj'),
    
	url(r'^editar_email/$', views.editar_email, name='accounts.editar_email'),
	url(r'^editar_perfil/$', views.editar_perfil, name='accounts.editar_perfil'),
	url(r'^editar_contrasena/$', views.editar_contrasena, name='accounts.editar_contrasena'),


	url(r'^registro/$',  views.registro_view, name='accounts.registro'),
	url(r'^registro/registro_eps/$', views.registro_eps_view, name='accounts.registro_eps'),
	url(r'^registro/registro_especialista/$', views.registro_especialista_view, name='accounts.registro_especialista'),
	url(r'^registro/registro_usuario/$', views.registro_usuario_view, name='accounts.registro_usuario'),
	url(r'^gracias/(?P<username>.+)$', views.gracias_view,  name='accounts.gracias'),
]
