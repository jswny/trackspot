from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('album/', views.album_main, name='album_main'),
    path('album/<int:pk>', views.album, name='album'),
    path('artist/<int:pk>', views.artist, name='artist'),
    path('song/<int:pk>', views.song, name='song'),
    path('user/<int:pk>', views.user, name='user'),
    path('user/<int:pk>/edit', views.edit_trackspotter.as_view(), name='edit_trackspotter'),
    path('user/<int:pk>/edit', views.edit_critic.as_view(), name='edit_critic')
]