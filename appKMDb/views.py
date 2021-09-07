import ipdb
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (ListCreateAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from appKMDb.permissions import NeverPermit, OnlyAdmin, OnlyCritico

from .models import Genre, Movie, Review
from .serializers import GenreSerializer, MovieSerializer, ReviewSerializer


class MovieViews(ListCreateAPIView):    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyAdmin, IsAuthenticatedOrReadOnly]
    
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewView(ListCreateAPIView):   
    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyCritico]


    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    

