from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Genre

# Create your models here.
class User(AbstractUser):
    # null=True 는 필드의 값이 NULL(정보 없음)로 저장되는 것을 허용
    # blank=True 는 필드가 폼(입력 양식)에서 빈 채로 저장되는 것을 허용(공백허용)
    like_genres = models.ManyToManyField(Genre, related_name='like_users', null=True)
    # accounts_user_genre_liker
    
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followings", blank=True)
    # 팔로워 팔로잉 기능