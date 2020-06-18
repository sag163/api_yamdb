from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Genre, Title, Review, Comment


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        # return {'name': obj.name, 'slug': obj.slug} # страница выдаёт ошибку unhashable type: 'dict'
        return f"'name': {obj.name}, 'slug': {obj.slug}" # эта строчка не проходит тесты из-за ковычек


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    category = CustomSlugRelatedField(queryset=Category.objects.all(), 
                                     slug_field='slug')
    genre = CustomSlugRelatedField(queryset=Genre.objects.all(),
                                   slug_field='slug',
                                   many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
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

