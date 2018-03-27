from django.db import models
from django.core.validators import MaxValueValidator
from django.urls import reverse

# TODO: integrate users/critics with Django admin stuff?

class Artist(models.Model):
    name = models.CharField(help_text='Enter a name for this artist', max_length=100)
    bio = models.CharField(help_text='Enter a description fot this artist', blank=True, max_length=500)
    # albums -- connected via album foreign keys

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('artist', args=[str(self.id)])

class Album(models.Model):
    name = models.CharField(help_text='Enter a name for this album', max_length=100)
    image_url = models.CharField(help_text='Enter a URL for the album art for this album', max_length=500, null=True)
    release_date = models.DateField(null=True)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    description = models.TextField(help_text='Enter a description for this album', blank=True, max_length=1000)
    # genres -- connected via genre foreign keys
    # songs -- connected via song foreign keys
    # reviews -- connected via review foreign keys

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('album', args=[str(self.id)])

class Song(models.Model):
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    name = models.CharField(help_text='Enter a name for this song', max_length=100)
    description = models.CharField(help_text='Enter a description for this song', blank=True, max_length=500)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    # reviews -- connected via review foreign keys

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('song', args=[str(self.id)])

class Genre(models.Model):
    name = models.CharField(help_text='Enter a name for this genre', max_length=100)
    # albums -- connected via album foreign keys
    # songs -- connected via song foreign keys
    
    def __str__(self):
        return self.name

class Review(models.Model):
    description = models.CharField(help_text='Enter a description for this song', max_length=500)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # allow nulls so that reviews for songs and albums can be differentiated
    album = models.ForeignKey('Album', on_delete=models.CASCADE, null=True)
    song = models.ForeignKey('Song', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.description

    def review_type(self):
        """Determines the type of the review.

        If both album and song are null then the return is null.
        Otherwise, returns the opposite of whichever field is null between album and song in string form.
        """
        if self.album is None and self.song is None:
            return None
        elif self.album is None:
            return 'song'
        elif self.song is None:
            return 'album'

class User(models.Model):
    name = models.CharField(help_text='Enter a name for this user', max_length=50)
    # reviews -- connected via review foreign keys
    bio = models.CharField(help_text='Enter a bio for this user', max_length=500)
    location = models.CharField(help_text='Enter a location for this user', max_length=50)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('user', args=[str(self.id)])

class Critic(User):
    # inherits all other field from User class
    organization = models.CharField(help_text='Enter a location for this critic', max_length=50)

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('critic', args=[str(self.id)])
