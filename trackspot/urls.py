from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('album/', views.album_main, name='album_main'),
    path('album/<int:pk>', views.album, name='album'),
    path('artist/<int:pk>', views.artist, name='artist'),
    path('song/<int:pk>', views.song, name='song'),
    path('user/<int:pk>', views.user, name='user'),
]

urlpatterns += [
	path('album/create/', views.AlbumCreate.as_view(), name='album_create'),
	path('album/<int:pk>/update/', views.AlbumUpdate.as_view(), name='album_update'),
	path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='album_delete'),
]