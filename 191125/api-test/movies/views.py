from django.shortcuts import render
from .models import Genre, Director, Grade, Movie

# Create your views here.
def index(request):
    genres = Genre.objects.all()
    directors = Director.objects.all()
    grades = Grade.objects.all()
    movies = Movie.objects.all()
    context = {
        'genres': genres,
        'directors': directors,
        'grades': grades,
        'movies': movies
    }
    return render(request, 'movies/index.html')