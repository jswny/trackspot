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

    review_critic = Review.objects.filter(album=album_id).exclude(user__critic=None)
    review_critic_count = Review.objects.filter(album=album_id).exclude(user__critic=None).count()
    review_critic_rating_perfect = 100    
    review_critic_rating_total = Review.objects.filter(album=album_id).exclude(user__critic=None).aggregate(Sum('rating'))['rating__sum']
    if review_critic_count == 0:
        review_critic_rating_average = 0
    else:
        review_critic_rating_average = float("{0:.1f}".format(review_critic_rating_total / review_critic_count))

    review_user = Review.objects.filter(album=album_id).filter(user__critic=None)
    review_user_count = Review.objects.filter(album=album_id).filter(user__critic=None).count()
    review_user_rating_perfect = 100    
    review_user_rating_total = Review.objects.filter(album=album_id).filter(user__critic=None).aggregate(Sum('rating'))['rating__sum']
    if review_user_count == 0:
        review_user_rating_average = 0
    else:
        review_user_rating_average = float("{0:.1f}".format(review_user_rating_total / review_user_count))

    if review_critic_count == 0 and review_user_count == 0:
        review_rating_overall = 0
    elif review_critic_count == 0 and review_user_count != 0:
        review_rating_overall = float("{0:.1f}".format((review_user_rating_total) / (review_user_count)))
    elif review_critic_count != 0 and review_user_count == 0:
        review_rating_overall = float("{0:.1f}".format((review_critic_rating_total) / (review_critic_count)))
    else:
        review_rating_overall = float("{0:.1f}".format((review_critic_rating_total + review_user_rating_total) / (review_critic_count + review_user_count)))

    return render(
        request,
        'trackspot/album.html',
        context = {
            'the_album':the_album,
            'song_list':song_list,
            'review_critic':review_critic,
            'review_critic_count':review_critic_count,
            'review_critic_rating_perfect':review_critic_rating_perfect,
            'review_critic_rating_total':review_critic_rating_total,
            'review_critic_rating_average':review_critic_rating_average,
            'review_user':review_user,
            'review_user_count':review_user_count,
            'review_user_rating_perfect':review_user_rating_perfect,
            'review_user_rating_total':review_user_rating_total,
            'review_user_rating_average':review_user_rating_average,
            'review_rating_overall':review_rating_overall
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

def user(request, **kwargs):
    user_id = kwargs['pk']
    return render(request, 'trackspot/user.html')