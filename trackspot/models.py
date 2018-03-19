from django.db import models
from django.core.validators import MaxValueValidator

# TODO: add string representations for each model
# TODO: add associations
# TODO: figure out which associations are not needed and update ERD as necessary (reference ERD from Mozilla models tutorial)

class Artist(models.Model):
    name = models.CharField(help_text="Enter a name for this artist", max_length=100)
    bio = models.CharField(help_text="Enter a description fot this artist", blank=True, max_length=500)
    # albums

class Album(models.Model):
    name = models.CharField(help_text="Enter a name for this album", max_length=100)
    release_date = models.DateField(null=True)
    # artists
    # genres
    # songs
    # reviews

class Song(models.Model):
    # album
    name = models.CharField(help_text="Enter a name for this song", max_length=100)
    description = models.CharField(help_text="Enter a description for this song", blank=True, max_length=500)
    # genre
    # reviews

class Genre(models.Model):
    name = models.CharField(help_text="Enter a name for this genre", max_length=100)
    # albums
    # songs

class Review(models.Model):
    description = models.CharField(help_text="Enter a description for this song", max_length=500)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    # user

class User(models.Model):
    name = models.CharField(help_text="Enter a name for this user", max_length=50)
    # reviews
    bio = models.CharField(help_text="Enter a bio for this user", max_length=500)
    location = models.CharField(help_text="Enter a location for this user", max_length=50)

class Critic(User):
    organization = models.CharField(help_text="Enter a location for this critic", max_length=50)
