from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Review(models.Model):
    title = models.TextField()
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    score = models.IntegerField(default=0, null=True, blank=True)
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)

class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)