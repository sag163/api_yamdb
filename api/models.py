from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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
    title = models.TextField()
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(default=0, null=True, blank=True)
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)
