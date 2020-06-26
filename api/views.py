from rest_framework import status, generics, viewsets, mixins, filters, permissions
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import (User, 
                    Category, 
                    Genre, 
                    Title, 
                    Review, 
                    Comment,
                    User)
from .serializers import (#UserRegistrationSerializer,
                        #MyAuthTokenSerializer,
                        UserSerializer,
                        CategorySerializer,
                        GenreSerializer,
                        TitleSerializer,
                        ReviewSerializer,
                        CommentSerializer,
                        )
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import generics
from rest_framework_simplejwt.views import (
    TokenObtainPairView,)
from django.shortcuts import render
from rest_framework.response import Response
from .pagination import CustomPagination
from django.shortcuts import get_object_or_404
from .permissions import IsAdminPermission, IsModeratorPermission, IsOwnerPermission
from rest_framework.pagination import PageNumberPagination

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


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
    permission_classes = [permissions.AllowAny]#, IsOwnerOrReadOnly]
  
   
    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs['titles_pk'])
        return title

    def get_queryset(self):
        queryset = Review.objects.filter(title=self.get_title())
        return queryset

    def update_rating(self):
        title = self.get_title()
        average_rating = Review.objects.filter(title=title).aggregate(Avg("score"))
        title.score = average_rating
        title.save()

    

    def perform_create(self, serializer):
        pk=self.kwargs.get("titles_pk")
        print('==========>>>>>', pk)
        title = get_object_or_404(Title, pk=self.kwargs.get("titles_pk"))
        print('==========>>>>>', title)
        review = Review.objects.filter(title_id=title.id, author=self.request.user)
        if self.request.method == 'POST' and review:
            raise ValidationError('Можно оставить только один отзыв на одно произведение.')
        serializer.save(author=self.request.user, title_id=self.kwargs.get("titles_pk"))
        self.update_rating()

    #def partial_update(self, request, titles_pk, pk=None):
    #    review = get_object_or_404(Review, pk=titles_pk)
    #    serializer = ReviewSerializer(review, data=request.data, partial=True)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, titles_pk, pk=None):
            if not request.user.is_authenticated:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            review = get_object_or_404(Review, pk=pk)
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if review.author != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            if serializer.is_valid():
                serializer.save(author=request.user, title_id=titles_pk)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, title_id, pk=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        review = get_object_or_404(Review, pk=pk)
        if review.author != request.user and request.user.role != 'moderator':
            return Response(status=status.HTTP_403_FORBIDDEN)
        review.delete()
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
        if comment.author != request.user:# and request.user.role != 'moderator':
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)