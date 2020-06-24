from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STATUS_CHOICESS = [
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    ]

    username = None
    email = models.EmailField(unique=True)
    confirmation_code = models.IntegerField(blank=True, null=True)
    role = models.CharField(choices=STATUS_CHOICESS, max_length=50, default='user')
    bio = models.CharField(max_length=500, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(default=0)
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
