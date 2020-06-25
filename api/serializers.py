from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Category, Genre, Title, Review, Comment
import random


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def generate_code():
    random.seed()
    return str(random.randint(10000000,99999999))


class UserSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("email",)
    
    def validate(self, data):
        confirmation_code = generate_code()
        data['confirmation_code'] = confirmation_code
        return data

class UserAvtorizaytion(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('email', 'confirmation_code',)

    def validate(self, data):
        email = data['email']
        confirmation_code = data['confirmation_code']
        profile = get_object_or_404(User, email=email)
        if profile.confirmation_code != confirmation_code:
            raise ValidationError('ошибка')
        else:
            token = get_tokens_for_user(profile)
            data['token'] = token
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug} # для успешного прохождения тесто
        #return value.name


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
