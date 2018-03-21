from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('album', views.album, name='album'),
    path('artist', views.artist, name='artist'),
    path('critic', views.critic, name='critic'),
    path('song', views.song, name='song'),
    path('user', views.user, name='user'),
]