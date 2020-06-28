import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import (viewsets, mixins, filters,
                            permissions, generics, status)

from .models import (User,
                     Category, Genre, Title,
                     Review, Comment)
from .serializers import (UserSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerializer, CommentSerializer,
                          SignUpSerializer, SignInSerializer)
from .filters import CustomFilterBackend
from .permissions import IsAdminUser, IsAdminOrReadOnlyPermission


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.confirmation_code = serializer.validated_data['confirmation_code']
            serializer.email = serializer.validated_data['email']
            serializer.save()
            print(serializer)
            send_mail(
                'Авторизация',
                f'confirmation_code = {serializer.confirmation_code} email = {serializer.email}',
                'mi@mi.mi',
                [f'{serializer.email}'],
                fail_silently=False,
            )
            return Response(serializer.data)


class SignInView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'token': serializer.validated_data['token']})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'username'


class UserMeViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    lookup_field = None

    def get_queryset(self):
        queryset = User.objects.filter(email=self.request.user).all()
        return queryset

    def get_object(self):
        obj = self.get_queryset().get()
        return obj


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnlyPermission]
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
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = [CustomFilterBackend]
    filterset_fields = ['category', 'genre', 'year', 'name']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs['titles_pk'])
        return title

    def get_queryset(self):
        queryset = Review.objects.filter(title=self.get_title())
        return queryset

    def update_rating(self):
        title = get_object_or_404(Title, id=self.kwargs['titles_pk'])
        average_rating = Review.objects.filter(title=title).aggregate(Avg("score"))
        print(average_rating)
        title.rating = round(average_rating['score__avg'], 1)
        print(title.rating)
        title.save()

    def perform_create(self, serializer):
        pk = self.kwargs.get("titles_pk")
        title = get_object_or_404(Title, pk=self.kwargs.get("titles_pk"))
        review = Review.objects.filter(title_id=title.id, author=self.request.user)
        if self.request.method == 'POST' and review:
            raise ValidationError('Можно оставить только один отзыв на одно произведение.')
        serializer.save(author=self.request.user, title_id=self.kwargs.get("titles_pk"))
        self.update_rating()

    def partial_update(self, request, titles_pk, pk=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if review.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save(author=request.user, title_id=titles_pk)
            self.update_rating()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, titles_pk, pk=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        review = get_object_or_404(Review, pk=pk)
        if review.author != request.user and request.user.role != 'moderator':
            return Response(status=status.HTTP_403_FORBIDDEN)
        review.delete()
        self.update_rating()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_review(self):
        review = get_object_or_404(Review, id=self.kwargs['review_pk'])
        return review

    def get_queryset(self):
        queryset = Comment.objects.filter(review=self.get_review()).all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_pk"))
        serializer.save(author=self.request.user, review_id=self.kwargs.get("review_pk"))

    def partial_update(self, request, titles_pk, review_pk, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save(author=request.user, review_id=review_pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, titles_pk, review_pk, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author != request.user and request.user.role != 'moderator':
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
