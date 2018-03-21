from django.shortcuts import render

# Create your views here.

from .models import *

def index(request):
    return render(request, 'trackspot/index.html')

def album(request):
    return render(request, 'trackspot/album.html')

def artist(request):
    return render(request, 'trackspot/artist.html')

def critic(request):
    return render(request, 'trackspot/critic.html')

def song(request):
    return render(request, 'trackspot/song.html')

def user(request):
    return render(request, 'trackspot/user.html')