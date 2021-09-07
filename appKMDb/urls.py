from django.urls import path

from appKMDb.views import MovieDetailView, MovieViews, ReviewView

urlpatterns = [
   
    path('movies/', MovieViews.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('movies/<int:pk>/review', ReviewView.as_view()),
    path('review/', ReviewView.as_view()),
    # path('review/<int:pk>/', MovieDetailView.as_view()),
    # path('movies/<int:id>/review', MovieViews.as_view()),
    # path('genre/', GenreView.as_view()),
    # path('genre/<int:pk>/', GenreView.as_view())


]
