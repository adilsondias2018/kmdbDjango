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

class CriticSerializerReview(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class GenreSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Genre
        fields = ['id','name']

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['id','critic', 'stars','review', 'spoilers']
    
    stars=serializers.IntegerField(min_value=1, max_value=10)
    

    print(stars)

    critic = CriticSerializerReview(read_only=True)      


class MovieSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)
    # id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Movie
        fields= '__all__'
        depth = 1

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        
        movie = Movie.objects.get_or_create(**validated_data)[0]

        for genre in genres_data:

            new_genre = Genre.objects.get_or_create(**genre)[0]
            movie.genres.add(new_genre)

        return movie

    def update(self, instance, validated_data):

        instance.name = validated_data['name']
        instance.save()
        return instance


class NoMovieReviewSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)
    # id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Movie
        # exclude = ['reviews']
        fields = ['id', 'title', 'duration','premiere', 'classification', 'synopsis', 'genres']
        depth = 1




    # def create(self,validated_data): 

    #     ipdb.set_trace()  
    #     user = User.objects.get(validated_data['user'])
    #     movie = Movie.objects.get(id=pk)        
    #     review = Review.objects.get_or_create(**validated_data)[0]
    #     movie.add(user)
    #     movie.add(review)
    
    #     return review


