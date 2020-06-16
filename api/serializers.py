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
        id = serializers.ReadOnlyField()
        genre = serializers.ReadOnlyField()
        category = serializers.ReadOnlyField()
        class Meta:
                fields = ('id', 'name', 'year', 'genre', 'category')
                model = Title


class ReviewSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source='author.username')
        class Meta:
                fields = ('title', 'text', 'author', 'score', 'pub_date')
                model = Review


class CommentSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source='author.username')
        class Meta:
                fields = ('review', 'text', 'author', 'pub_date')
                model = Comment

