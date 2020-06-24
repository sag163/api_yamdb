from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Category, Genre, Title, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, value):
        #return {'name': value.name, 'slug': value.slug} # для успешного прохождения тесто
        return value.name


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

