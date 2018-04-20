from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('album/', views.album_main, name='album_main'),
    path('album/<int:pk>', views.album, name='album'),
    path('artist/<int:pk>', views.artist, name='artist'),
    path('song/<int:pk>', views.song, name='song'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user'),
    path('login/<int:pk>', views.login, name='login'),
    path('user/<int:pk>', views.user, name='user'),
    path('user/edit_trackspotter', views.edit_trackspotter.as_view(), name='edit_trackspotter'),
    path('user/edit_critic', views.edit_critic.as_view(), name='edit_critic'),
	re_path(r'^search/$', views.search, name='search'),
]

urlpatterns += [
	path('album/create/', views.AlbumCreate.as_view(), name='album_create'),
	path('album/<int:pk>/update/', views.AlbumUpdate.as_view(), name='album_update'),
	path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='album_delete'),
	path('song/create/', views.SongCreate.as_view(), name='song_create'),
	path('song/<int:pk>/update/', views.SongUpdate.as_view(), name='song_update'),
	path('song/<int:pk>/delete/', views.SongDelete.as_view(), name='song_delete'),
	path('artist/create/', views.ArtistCreate.as_view(), name='artist_create'),
	path('artist/<int:pk>/update/', views.ArtistUpdate.as_view(), name='artist_update'),
	path('artist/<int:pk>/delete/', views.ArtistDelete.as_view(), name='artist_delete'),
	path('album/<int:pk>/reviewcreate/', views.create_album_review, name = 'album_review_create'),
	path('song/<int:pk>/reviewcreate/', views.create_song_review, name = 'review_form'),
]

