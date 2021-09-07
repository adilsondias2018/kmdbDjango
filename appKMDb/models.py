from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    premiere = models.CharField(max_length=50)
    classification = models.IntegerField()
    synopsis = models.CharField(max_length=255)
 
 
class Genre(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ManyToManyField(Movie, related_name='geners' )



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    movie = models.ForeignKey(Movie, on_delete=CASCADE)
    stars = models.IntegerField()
    review = models.CharField(max_length=255)
    spoilers = models.BooleanField()






