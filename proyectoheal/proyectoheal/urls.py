# coding=utf-8
"""proyectoheal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
# Añade esto, al inicio del documento
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #URL del Administrador del Sitio (Usuario Programador)
    url(r'^$', include('home.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^agenda/', include('agenda.urls')),
    url(r'^admin/', include(admin.site.urls)),

]

# Añade esto, al final del documento
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns.append(
        # /media/:<mixed>path/
        url(
            regex=r'^media/(?P<path>.*)$',
            view='django.views.static.serve',
            kwargs={'document_root': settings.MEDIA_ROOT}))