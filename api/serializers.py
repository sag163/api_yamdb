from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
     class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
     class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
  

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
   
    class Meta:
        fields = ('id', 'review', 'text', 'author', 'score', 'pub_date')
        model = Comment

