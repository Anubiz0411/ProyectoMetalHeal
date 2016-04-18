# home/urls.py
 # coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    # /home/
    url(r'^$', view=views.index_view, name='home.index'),
    url(r'^about/$', view=views.AboutView, name='home.about'),
    url(r'^contact/$', view=views.ContactView.as_view(), name='home.contact'),
]