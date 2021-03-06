from django.shortcuts import render
from django.db.models import Count
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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
    
    critics = Group.objects.get(name='Critics')
    trackspotters = Group.objects.get(name='Trackspotters')

    # Critic Review
    review_critic = Review.objects.filter(album=album_id).filter(user__groups=critics)
    review_critic_count = review_critic.count()
    review_critic_rating_perfect = 100    
    review_critic_rating_total = review_critic.aggregate(Sum('rating'))['rating__sum']
    if review_critic_count == 0:
        review_critic_rating_average = 0
    else:
        review_critic_rating_average = float("{0:.1f}".format(review_critic_rating_total / review_critic_count))

    # User Review
    review_user = Review.objects.filter(album=album_id).filter(user__groups=trackspotters)
    review_user_count = review_user.count()
    review_user_rating_perfect = 100    
    review_user_rating_total = review_user.aggregate(Sum('rating'))['rating__sum']
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

    albums_same_genre = []
    top_songs = []
    
    for album in albums:
        genre = album.genre
        albums_same_genre = Album.objects.filter(genre=genre)

        critics = Group.objects.get(name='Critics')
        trackspotters = Group.objects.get(name='Trackspotters')

        user_reviews = Review.objects.filter(album=album.id).filter(user__groups=trackspotters)
        critic_reviews = Review.objects.filter(album=album.id).filter(user__groups=critics)
        
        user_count = user_reviews.count()
        user_total_rating = user_reviews.aggregate(Sum('rating'))['rating__sum']
        critic_count = critic_reviews.count()
        critic_total_rating = critic_reviews.aggregate(Sum('rating'))['rating__sum']
        
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

            user_song_reviews = Review.objects.filter(song=song.id).filter(user__groups=trackspotters)
            critic_song_reviews = Review.objects.filter(song=song.id).filter(user__groups=critics)
        
            user_song_count = Review.objects.filter(song=song.id).filter(user__groups=trackspotters).count()
            user_song_total_rating = Review.objects.filter(song=song.id).filter(user__groups=trackspotters).aggregate(Sum('rating'))['rating__sum']
            critic_song_count = Review.objects.filter(song=song.id).filter(user__groups=critics).count()
            critic_song_total_rating = Review.objects.filter(song=song.id).filter(user__groups=critics).aggregate(Sum('rating'))['rating__sum']


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


def song(request, **kwargs):
    song_id = kwargs['pk']
    song = Song.objects.get(pk=song_id)
    album_songs = Song.objects.filter(album__id = song.album.id)
    review_user_rating_perfect = 100

    critics = Group.objects.get(name='Critics')
    trackspotters = Group.objects.get(name='Trackspotters')

    song_reviews_users = Review.objects.filter(song__id=song.id).filter(user__groups=trackspotters)
    song_reviews_critics = Review.objects.filter(song__id=song.id).filter(user__groups=critics)
    
    review_user_count_critic = song_reviews_critics.count()
    review_user_rating_total_critic = song_reviews_critics.aggregate(Sum('rating'))['rating__sum']
    if(review_user_count_critic != 0):
        review_user_rating_average_critic = int(round(review_user_rating_total_critic / review_user_count_critic))
    else:
        review_user_rating_average_critic = 'No Reviews'
    
    review_user_count_user = song_reviews_users.count()
    review_user_rating_total_user = song_reviews_users.aggregate(Sum('rating'))['rating__sum']
    if(review_user_count_user != 0):
        review_user_rating_average_user = int(round(review_user_rating_total_user / review_user_count_user))
    else:
        review_user_rating_average_user = 'No Reviews'
    
    return render(
        request, 
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
def login(request, **kwargs):
    login_id = kwargs['pk']
    return render(
        request,
        'trackspot/login.html',
        context = {
        }
    )
        



def user(request, **kwargs):
    user_id = kwargs['pk']
    user = User.objects.get(pk=user_id)
    is_current_user = user_id == request.user.id
    
    return render(
        request, 
        'trackspot/user.html',
        context = {
            'user': user,
            'is_current_user': is_current_user,
        }
    )

class UserDetailView(generic.DetailView):
    # user_id = kwargs['pk']
    model = User
    template_name='trackspot/user.html'

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView


class edit_trackspotter(UpdateView):
    model = Profile
    fields = {'name', 'bio', 'location', 'profile_pic'}
    initial = {'name': '', 'location': '', 'bio': '', 'profile_pic': ''}

    def get_success_url(self):
       user_id=self.request.user.id
       return reverse('user', kwargs={'pk':user_id})

    def get_object(self):
        return Profile.objects.get(pk=self.request.user.profile.id)

class edit_critic(UpdateView):
    model = Profile
    fields = {'name', 'bio', 'location', 'profile_pic', 'organization'}
    initial = {'name': '', 'location': '', 'bio': '', 'profile_pic': '', 'organization': ''}

    def get_success_url(self):
       user_id=self.request.user.id
       return reverse('user', kwargs={'pk':user_id})
    def get_object(self):
        return Profile.objects.get(pk=self.request.user.profile.id)
#def edit_profile(request, pk):
#    user_instance = get_object_or_404(User, pk=pk)
#    if request.method == 'POST':
#        form = user_profile_form(request.POST)
#        if form.is_valid():
#            user_instance.name = form.cleaned_data['name']
#            user_instance.location = form.cleaned_data['location']
#            user_instance.bio = form.cleaned_data['bio']
#            user_instance.profile_pic = form.cleaned_data['profile_pic']
#            user_instance.save()
#            return HttpResponseRedirect(reverse('user'))
#    else:
#        form = user_profile_form(initial={'name': '', 'location': '', 'bio': '', 'profile_pic': ''})
#    return render(request, 'trackspot/edit_profile_form.html', {'form': form, 'user_instance': user_instance})
# Hook pages to forms
# Album
class AlbumCreate(CreateView):
    model = Album
    fields = '__all__'

class AlbumUpdate(UpdateView):
    model = Album
    fields = '__all__'

class AlbumDelete(DeleteView):
    model = Album

# Song
class SongCreate(CreateView):
    model = Song
    fields = '__all__'

class SongUpdate(UpdateView):
    model = Song
    fields = '__all__'

class SongDelete(DeleteView):
    model = Song

# Artist
class ArtistCreate(CreateView):
    model = Artist
    fields = '__all__'

class ArtistUpdate(UpdateView):
    model = Artist
    fields = '__all__'

class ArtistDelete(DeleteView):
    model = Artist

from .forms import review_form

def create_song_review(request, pk):
    song = get_object_or_404(Song, pk = pk)
    review = Review()

    # If this is a POST request then proces the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = review_form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            print(form.cleaned_data)
            review.user = request.user
            review.rating = form.cleaned_data['rating']
            review.description = form.cleaned_data['description']
            review.song_id = pk
            review.save()

            # redirect to a new URL:
            user_id = request.user.id
            return HttpResponseRedirect(reverse('user', kwargs={'pk':user_id}))

    # If this is a GET (or any other method) create the default form.
    else:
        form = review_form(initial={'review': '', 'rating': ''})
    return render(request, 'trackspot/review_form.html', {'form': form, 'review': review})

def create_album_review(request, pk):
    album = get_object_or_404(Album, pk = pk)
    review = Review()

    # If this is a POST request then proces the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = review_form(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            print(form.cleaned_data)
            review.user = request.user
            review.rating = form.cleaned_data['rating']
            review.description = form.cleaned_data['description']
            review.album_id = pk
            review.save()

            # redirect to a new URL:
            user_id = request.user.id
            return HttpResponseRedirect(reverse('user', kwargs={'pk':user_id}))

    # If this is a GET (or any other method) create the default form.
    else:
        form = review_form(initial={'review': '', 'rating': ''})
    return render(request, 'trackspot/review_form.html', {'form': form, 'review': review})

def search(request):
    query = request.GET.get('q')

    artists = Artist.objects.filter(name__contains=query)
    albums = Album.objects.filter(name__contains=query)
    songs = Song.objects.filter(name__contains=query)
    critics = User.objects.filter(groups__name='Critics').filter(profile__name__contains=query)
    trackspotters = User.objects.filter(groups__name='Trackspotters').filter(profile__name__contains=query)

    return render(
        request, 
        'trackspot/search.html', 
        {
            'query': query,
            'artists': artists,
            'albums': albums,
            'songs': songs,
            'critics': critics,
            'trackspotters': trackspotters,
        }
    )
