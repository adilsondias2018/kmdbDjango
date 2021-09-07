import ipdb
from account.serializers import UserSerializer
from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.query_utils import PathInfo
from rest_framework import serializers

from .models import Genre, Movie, Review

# class AccountSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         models: User
#         fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']




class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ['name']


class MovieSerializer(serializers.ModelSerializer):
    geners = GenreSerializer(many=True)
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Movie
        fields= '__all__'
        depth = 1

    def create(self, validated_data):
        genres_data = validated_data.pop('geners')
        
        movie = Movie.objects.get_or_create(**validated_data)[0]

        for genre in genres_data:

            new_genre = Genre.objects.get_or_create(**genre)[0]
            movie.geners.add(new_genre)

        return movie

    def update(self, instance, validated_data):

        instance.name = validated_data['name']
        instance.save()
        return instance


        
class ReviewSerializer(serializers.ModelSerializer):
    # ipdb.set_trace()
    user = UserSerializer()
    class Meta:
        model = Review
        fields = '__all__'
    
    def create (self, pk, validated_data):        
        movie = Movie.objects.get(id=pk)        
        review = Review.objects.get_or_create(**validated_data)
        movie.add(review)
    
        return review




