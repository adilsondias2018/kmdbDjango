from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=255)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    premiere = models.CharField(max_length=50)
    classification = models.IntegerField()
    synopsis = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=CASCADE)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    movie = models.ForeignKey(Movie, on_delete=CASCADE)

    


