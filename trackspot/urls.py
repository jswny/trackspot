from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('album/', views.album_main, name='album_main'),
    path('album/<int:pk>', views.album, name='album'),
    path('artist/<int:pk>', views.artist, name='artist'),
    path('critic/<int:pk>', views.critic, name='critic'),
    path('song/<int:pk>', views.song, name='song'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user'),
]