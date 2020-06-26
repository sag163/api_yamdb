from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import User, Category, Genre, Title, Review, Comment, User
import random, string, base64
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from urllib.parse import quote
from django.db.models import Avg



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
     class Meta:
        fields = ('name', 'slug')
        model = Genre


#class TitleSerializer(serializers.ModelSerializer):
#        id = serializers.ReadOnlyField()
#        genre = serializers.ReadOnlyField()
#        category = serializers.ReadOnlyField()
#        class Meta:
#                fields = ('id', 'name', 'year', 'genre', 'category')
#                model = Title   


#class CustomSlugRelatedField(serializers.SlugRelatedField):
#    def to_representation(self, obj):
        # return {'name': obj.name, 'slug': obj.slug} # страница выдаёт ошибку unhashable type: 'dict'
 #       return f"'name': {obj.name}, 'slug': {obj.slug}" # эта строчка не проходит тесты из-за ковычек

#class TitleSerializer(serializers.ModelSerializer):
    #rating = serializers.ReadOnlyField()
##    #rating= Review.objects.filter(title_id=title.id).aggregate(Avg("score"))
#    category = CustomSlugRelatedField(queryset=Category.objects.all(), 
#                                     slug_field='slug')
#    genre = CustomSlugRelatedField(queryset=Genre.objects.all(),
#                                   slug_field='slug',
#                                   many=True)


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, value):
        #return {'name': value.name, 'slug': value.slug}
        return value.slug

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

 #   class Meta:
 #       fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
 #       model = Title   

  #  def average_rating(self, title):
 #       rating = Review.objects.filter(title_id=title.id).aggregate(Avg("score"))
 #       return rating

class ReviewSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source='author.username')
        title = serializers
        class Meta:
                fields = ('id', 'text', 'author', 'score', 'pub_date')
                model = Review


class CommentSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source='author.username')
        class Meta:
                fields = ('id', 'text', 'author', 'pub_date')
                model = Comment

