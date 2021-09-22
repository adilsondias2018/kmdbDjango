import ipdb
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (ListCreateAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from appKMDb.permissions import NeverPermit, OnlyAdmin, OnlyCritico

from .models import Genre, Movie, Review
from .serializers import (GenreSerializer, MovieSerializer,
                          NoMovieReviewSerializer, ReviewSerializer)


class MovieViews(ListCreateAPIView):    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, OnlyAdmin]

    def get_queryset(self):

        if 'title' in self.request.GET:
            
            return Movie.objects.filter(title__contains=self.request.GET['title'])
        
        return self.queryset.all()



    
    # pagination_class = CustomPagination
    
    # def get_serializer_class(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         return super().get_serializer_class()
    #     return MovieSerializer
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
        
    #     user = self.request.user
        
    #     if user.is_authenticated:
    #         return queryset.filter(owner=user)
        
    #     return queryset.filter(owner__isnull=True)
            
# class GenreView(ListCreateAPIView):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer

class MovieDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, OnlyAdmin]

    queryset = Movie.objects.all()    
    serializer_class = MovieSerializer

    def get_serializer_class(self):

        if self.request.user.is_anonymous:
            return NoMovieReviewSerializer
        
        return self.serializer_class
        


            


class ReviewView(ListCreateAPIView, UpdateAPIView):   
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyCritico]

    lookup_url_kwarg = "movie_id"

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):       
        if self.request.user.is_superuser == False:
            return Review.objects.filter(critic = self.request.user)

        return self.queryset.all()
    
    def create(self,request, *args, **kwargs): 

        # ipdb.set_trace()  
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # request.data['stars'] = serializers.IntegerField(min_value=1, max_value=10)
        
        headers = self.get_success_headers(serializer.data)
        
        user = User.objects.get(id = request.user.id)
        movie = get_object_or_404(Movie, id=kwargs['movie_id'])   
        

        if not User.objects.filter(id=user.id).exists():

            return Response(status=status.HTTP_404_NOT_FOUND)

        if not Movie.objects.filter(id=movie.id).exists():

            return Response(status=status.HTTP_404_NOT_FOUND)

        if Review.objects.filter(critic = user, movie=movie).exists():
            return Response({'detail': 'You already made this review.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)       
        review = Review.objects.get_or_create(**request.data, critic=user, movie=movie)[0]
        # movie.add(user)
        # movie.add(review)

        serializer = ReviewSerializer(review)
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):


        movie = get_object_or_404(Movie, id=kwargs['movie_id'])       

        user = User.objects.get(id = request.user.id)
        
        if not User.objects.filter(id=user.id).exists():

            return Response(status=status.HTTP_404_NOT_FOUND)

        if not Movie.objects.filter(id=movie.id).exists():

            return Response(status=status.HTTP_404_NOT_FOUND)

        if not Review.objects.filter(critic = user, movie=movie).exists():
            return Response({'detail': 'You already made this review.'}, status=status.HTTP_404_NOT_FOUND)


        partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        instance = Review.objects.filter(critic = user, movie=movie).first() 
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
      

        return Response(serializer.data)

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, OnlyCritico]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def update(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, id=kwargs['movie_id'])    
        user = User.objects.get(id = request.user.id)

        if not Movie.objects.filter(id=movie.id).exists():

            return Response(status=status.HTTP_404_NOT_FOUND)

        if not Review.objects.filter(critic = user, movie=movie).exists():
            return Response({"msg": "critica existente"}, status=status.HTTP_404_NOT_FOUND)


        partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        instance = Review.objects.filter(critic = user, movie=movie).first() 
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
    

        return Response(serializer.data)

    # def perform_update(self, serializer):
    #     serializer.save()

    

# class :
#     """
#     Create a model instance.
#     """
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save()

#     def get_success_headers(self, data):
#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}
