from django.db import models
from django.contrib.auth import settings

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=45)
    def __str__(self):
        return "{}. {}".format(self.id, self.name)

class Grade(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return "{}. {}".format(self.id, self.name)

class Genre(models.Model):
    name = models.CharField(max_length=150)
    # like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_genres', null=True, blank=True)
    def __str__(self):
        return "{}. {}".format(self.id, self.name)

class Movie(models.Model):
    title = models.CharField(max_length=150)
    title_en = models.CharField(max_length=150)
    summary = models.TextField()
    score = models.FloatField()
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=500)
    video_url = models.CharField(max_length=500, null=True)
    ost_url = models.CharField(max_length=500, null=True)

    movie_directors =  models.ManyToManyField(Director, related_name='director_movies')
    movie_genres = models.ManyToManyField(Genre, related_name='genre_movies')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    movie_like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_like_movies", null=True, blank=True)
    # 영화 좋아요
    def __str__(self):
        return "{}. {}".format(self.id, self.title)