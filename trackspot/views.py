from django.shortcuts import render
from django.db.models import Count
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic

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
    return render(request, 'trackspot/artist.html')

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
    return render(request, 'trackspot/song.html')

class UserDetailView(generic.DetailView):
    # user_id = kwargs['pk']
    model = User
    template_name='trackspot/user.html'