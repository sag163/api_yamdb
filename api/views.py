from rest_framework import viewsets, mixins, filters, permissions
from django.shortcuts import render
from rest_framework.response import Response
from .models import (User, 
                    Category, 
                    Genre, 
                    Title, 
                    Review, 
                    Comment,
                    User)
from .serializers import (UserRegistrationSerializer,
                        UserSerializer,
                        CategorySerializer,
                        GenreSerializer,
                        TitleSerializer,
                        ReviewSerializer,
                        CommentSerializer,
                        )
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import generics
from rest_framework_simplejwt.views import (
    TokenObtainPairView,)
from rest_framework.pagination import PageNumberPagination



class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
        ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination    

class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug', ]
    lookup_field = 'slug'

class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug', ] 
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'genre', 'year', ]
    search_fields = ['name', ]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]#, IsOwnerOrReadOnly]

    #def list(self, requests, titles_pk):
    #    review = Review.objects.filter(title=titles_pk)
    #    serializer = ReviewSerializer(review, many=True)
    #    return Response(serializer.data)
    
   
    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs['titles_pk'])
        return title
    def get_queryset(self):
        queryset = Review.objects.filter(title=self.get_title()).all()
        return queryset
    def update_rating(self):
        title = self.get_title()
        average_rating = Review.objects.filter(title=title).aggregate(Avg("score"))
        title.score = average_rating
        title.save()
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        self.update_rating()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        queryset = Review.objects.filter(title=self.get_post()).all()

