from django.contrib import admin
from .models import Genre, Director, Grade, Movie

# Register your models here.
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Grade)
admin.site.register(Movie)
