from rest_framework.response import Response
from rest_framework.views import APIView
import random
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, mixins, filters, permissions, generics
from .models import (User,
                     Category, 
                     Genre, 
                     Title, 
                     Review, 
                     Comment)
from .serializers import (UserSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          UserSerializers,
                          UserAvtorizaytion)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404





class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.confirmation_code = serializer.validated_data['confirmation_code']
            serializer.email = serializer.validated_data['email']
            serializer.save()
            print(serializer)
            send_mail(
                'Авторизация',
                f'Для авторизации перейдите по ссылке "http://127.0.0.1:8000/api/v1/auth/token/" с параметрами: confirmation_code = {serializer.confirmation_code} email = {serializer.email}',
                'mi@mi.mi',
                [f'{serializer.email}'],
                fail_silently=False,
            )
            return Response(serializer.data)

class Avtorizeytion(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserAvtorizaytion(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'token': serializer.validated_data['token']})

     
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'username'


class UserMeViewSet(mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = get_object_or_404(User, id=self.request.user.id)
class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'genre', 'year', ]
    search_fields = ['name', ]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def list(self, requests, titles_pk):
        review = Review.objects.filter(title=titles_pk)
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        