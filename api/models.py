from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.contrib.auth import get_user_model


class User(AbstractUser):
    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=16, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True)
    genre = models.ForeignKey(Genre,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)


class Comment(models.Model):
    review = models.ForeignKey( 
        Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)
