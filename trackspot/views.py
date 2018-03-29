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

    # Critic Review
    review_critic = Review.objects.filter(album=album_id).exclude(user__critic=None)
    review_critic_count = Review.objects.filter(album=album_id).exclude(user__critic=None).count()
    review_critic_rating_perfect = 100    
    review_critic_rating_total = Review.objects.filter(album=album_id).exclude(user__critic=None).aggregate(Sum('rating'))['rating__sum']
    if review_critic_count == 0:
        review_critic_rating_average = 0
    else:
        review_critic_rating_average = float("{0:.1f}".format(review_critic_rating_total / review_critic_count))

    # User Review
    review_user = Review.objects.filter(album=album_id).filter(user__critic=None)
    review_user_count = Review.objects.filter(album=album_id).filter(user__critic=None).count()
    review_user_rating_perfect = 100    
    review_user_rating_total = Review.objects.filter(album=album_id).filter(user__critic=None).aggregate(Sum('rating'))['rating__sum']
    if review_user_count == 0:
        review_user_rating_average = 0
    else:
        review_user_rating_average = float("{0:.1f}".format(review_user_rating_total / review_user_count))

    # Overall Score
    if review_critic_count == 0 and review_user_count == 0:
        review_rating_overall = 0
    elif review_critic_count == 0 and review_user_count != 0:
        review_rating_overall = float("{0:.1f}".format((review_user_rating_total) / (review_user_count)))
    elif review_critic_count != 0 and review_user_count == 0:
        review_rating_overall = float("{0:.1f}".format((review_critic_rating_total) / (review_critic_count)))
    else:
        review_rating_overall = float("{0:.1f}".format((review_critic_rating_total + review_user_rating_total) / (review_critic_count + review_user_count)))

    # Variable used in django template
    list = []
    for i in range(0,100):
        list.append(i)

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
            'review_rating_overall':review_rating_overall,
            'list':list
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
    albums = Album.objects.filter(artist__id=artist_id)


    for album in albums:
        genre = album.genre
        albums_same_genre = Album.objects.filter(genre=genre)

        user_reviews = Review.objects.filter(album=album.id).filter(user__critic=None)
        critic_reviews = Review.objects.filter(album=album.id).exclude(user__critic=None)
        
        user_count = Review.objects.filter(album=album.id).filter(user__critic=None).count()
        user_total_rating = Review.objects.filter(album=album.id).filter(user__critic=None).aggregate(Sum('rating'))['rating__sum']
        critic_count = Review.objects.filter(album=album.id).exclude(user__critic=None).count()
        critic_total_rating = Review.objects.filter(album=album.id).exclude(user__critic=None).aggregate(Sum('rating'))['rating__sum']
        
        if(critic_count != 0):
            album.critic_score = int(round(critic_total_rating/critic_count))
        else:
            album.critic_score = 'None'
        if(user_count != 0):
            album.user_score = int(round(user_total_rating/user_count))
        else:
            album.user_score = 'None'

        i=0
        top_songs = []
        for song in Song.objects.filter(album=album.id):

            user_song_reviews = Review.objects.filter(song=song.id).filter(user__critic=None)
            critic_song_reviews = Review.objects.filter(song=song.id).exclude(user__critic=None)
        
            user_song_count = Review.objects.filter(song=song.id).filter(user__critic=None).count()
            user_song_total_rating = Review.objects.filter(song=song.id).filter(user__critic=None).aggregate(Sum('rating'))['rating__sum']
            critic_song_count = Review.objects.filter(song=song.id).exclude(user__critic=None).count()
            critic_song_total_rating = Review.objects.filter(song=song.id).exclude(user__critic=None).aggregate(Sum('rating'))['rating__sum']


            if(critic_song_count != 0):
                song_critic_rating = int(round(critic_song_total_rating/critic_song_count))
                if(song_critic_rating>70):
                    top_songs.append(song)
                    i+=1
            else:
                song_critic_rating = 'None'
            if(user_song_count != 0):
                song_user_rating = int(round(user_song_total_rating/user_song_count))
            else:
                song_user_rating = 'None'


    return render(request, 
        'trackspot/artist.html', 
        context = {
        'artist':artist,
        'albums':albums,
        'albums_same_genre':albums_same_genre,
        'top_songs':top_songs
        }
    )
    

def critic(request, **kwargs):
    critic_id = kwargs['pk']
    curr_critic = Critic.objects.get(pk=critic_id)
    critics = Critic.objects.exclude(id=critic_id)
    song_reviews = Review.objects.filter(user__id=critic_id)
    critic_id1 = critic_id
    total_rating = Review.objects.filter(user__id=critic_id1).aggregate(Sum('rating'))['rating__sum']
    review_count = Review.objects.filter(user__id=critic_id1).count()
    if review_count == 0:
     average_rating = 0
    else:
        average_rating = float("{0:.1f}".format(total_rating / review_count))
    return render(request, 'trackspot/critic.html', 
        context = {
        'critics':critics,
        'song_reviews':song_reviews,
        'curr_critic':curr_critic,
        'review_count':review_count,
        'total_rating':total_rating,
        'average_rating':average_rating
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


class UserDetailView(generic.DetailView):
    # user_id = kwargs['pk']
    model = User
    template_name='trackspot/user.html'