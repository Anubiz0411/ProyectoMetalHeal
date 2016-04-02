# home/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    # /home/
    url(r'^$', view=views.index_view, name='home.index'),
]