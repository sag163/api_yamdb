from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (CategoryViewSet, GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet)
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
review_router = routers.NestedSimpleRouter(router, r'titles', lookup='titles')
review_router.register(r'reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(review_router.urls)),
]



