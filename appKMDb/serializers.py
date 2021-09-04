from django.contrib.auth.models import User
from rest_framework import generics

from .models import Genre, Movie, Review


class GenreSerializer(serialize.ModelSerializer):
    