from django.shortcuts import render
from django.db.models import Count
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

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
    the_album = Album.objects.all()[album_id-1]
    song_list = Song.objects.filter(album=album_id)

    review_user = Review.objects.filter(album=album_id)
    review_user_count = Review.objects.filter(album=album_id).count()
    review_user_rating_perfect = 100    
    review_user_rating_total = Review.objects.filter(album=album_id).aggregate(Sum('rating'))['rating__sum']
    review_user_rating_average = review_user_rating_total / review_user_count

    return render(
        request,
        'trackspot/album.html',
        context = {
            'the_album':the_album,
            'song_list':song_list,
            'review_user':review_user,
            'review_user_count':review_user_count,
            'review_user_rating_perfect':review_user_rating_perfect,
            'review_user_rating_total':review_user_rating_total,
            'review_user_rating_average':review_user_rating_average
        }
    )

def album_main(request, **kwargs):
    albums = Album.objects.all()
    return render(
        request,
        'trackspot/album_main.html',
        context = {
            'albums':albums
        }
    )

def artist(request, **kwargs):
    artist_id = kwargs['pk']
    artist = Artist.objects.get(pk=artist_id)
    albums = Album.objects.filter(artist__id=artist)
    return render(request, 
    	'trackspot/artist.html', 
    	context = {
    	'artist':artist
    	'albums':albums
    	}
    )
    

def critic(request, **kwargs):
    critic_id = kwargs['pk']
    critics = Critic.objects.all()
    return render(request, 'trackspot/critic.html', 
        context = {
        'critics':critics
        }
        )


def song(request, **kwargs):
    song_id = kwargs['pk']
    song = Song.objects.get(pk=song_id)
    album_songs = Song.objects.filter(album__id = song.album.id)
    review_user_rating_perfect = 100
    song_reviews_users = Review.objects.filter(song__id=song.id).filter(user__critic=None)
    song_reviews_critics = Review.objects.filter(song__id=song.id).exclude(user__critic=None)
	
	
    review_user_count_critic = Review.objects.filter(song=song_id).exclude(user__critic=None).count()
    review_user_rating_total_critic = Review.objects.filter(song=song_id).exclude(user__critic=None).aggregate(Sum('rating'))['rating__sum']
    if(review_user_count_critic != 0):
        review_user_rating_average_critic = int(round(review_user_rating_total_critic / review_user_count_critic))
    else:
        review_user_rating_average_critic = 'No Reviews'
	
    review_user_count_user = Review.objects.filter(song=song_id).filter(user__critic=None).count()
    review_user_rating_total_user = Review.objects.filter(song=song_id).filter(user__critic=None).aggregate(Sum('rating'))['rating__sum']
    if(review_user_count_user != 0):
        review_user_rating_average_user = int(round(review_user_rating_total_user / review_user_count_user))
    else:
	    review_user_rating_average_user = 'No Reviews'
	
    return render(request, 
	'trackspot/song.html',
	context = {
	'song':song,
    'album_songs':album_songs,
    'song_reviews_users':song_reviews_users,
    'song_reviews_critics':song_reviews_critics,
    'review_user_rating_average_critic':review_user_rating_average_critic,
    'review_user_rating_average_user':review_user_rating_average_user,
	'review_user_rating_perfect':review_user_rating_perfect
	}
	)

def user(request, **kwargs):
    user_id = kwargs['pk']
    return render(request, 'trackspot/user.html')