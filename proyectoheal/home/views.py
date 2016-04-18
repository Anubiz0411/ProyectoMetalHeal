# home/views.py

from django.shortcuts import render
from django.utils import timezone
from django.template import RequestContext

def index_view(request):
    return render(request, 'home/index.html')