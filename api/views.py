from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.response import Response
from .models import Category, Genre, Title, Review
from .serializers import (CategorySerializer,
                         GenreSerializer,
                         TitleSerializer,
                         ReviewSerializer)

class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    #def list(self, requests, title_id):
    #    review = Review.objects.filter(title=title_id)
    #    serializer = ReviewSerializer(review, many=True)
    #    return Response(serializer.data)


