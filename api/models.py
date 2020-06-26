from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from .managers import UserManager


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.text

class Comment(models.Model):
    review = models.ForeignKey( 
        Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text