from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
  

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
   
    class Meta:
        fields = ('id', 'review', 'text', 'author', 'score', 'pub_date')
        model = Comment

