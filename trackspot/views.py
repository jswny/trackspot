from django.shortcuts import render
from django.db.models import Count

# Create your views here.

from .models import *
import datetime

def get_current_album_releases():
    """
    Gets all of the albums which have release dates less than today,
    which means that they have been released so far and aren't being released
    in the future.
    """
    today = datetime.date.today()
    return Album.objects.filter(release_date__lte=today)

def get_future_album_releases():
    """
    Gets all of the albums which have release dates greater than today,
    which means that they have not been released yet.
    """
    today = datetime.date.today()
    return Album.objects.filter(release_date__gt=today)

# TODO: link items via URLs
def index(request):
    today = datetime.date.today()
    new_releases = get_current_album_releases().order_by('release_date')[:5]
    upcoming_releases = get_future_album_releases().order_by('release_date')[:5]
    trending = Song.objects.all().annotate(review_count=Count('review')).order_by('review_count')

    return render(
        request, 
        'trackspot/index.html',
        context = {
            'new_releases':new_releases,
            'upcoming_releases':upcoming_releases,
            'trending':trending
        }
    )

def album(request, **kwargs):
    album_id = kwargs['pk']
    return render(request, 'trackspot/album.html')

def artist(request, **kwargs):
    artist_id = kwargs['pk']
    return render(request, 'trackspot/artist.html')

def critic(request, **kwargs):
    critic_id = kwargs['pk']
    return render(request, 'trackspot/critic.html')

def song(request, **kwargs):
    song_id = kwargs['pk']
    song = Song.objects.get(pk=song_id)
    return render(request, 
	'trackspot/song.html',
	context = {
	'song':song
	}
	)

def user(request, **kwargs):
    user_id = kwargs['pk']
    return render(request, 'trackspot/user.html')