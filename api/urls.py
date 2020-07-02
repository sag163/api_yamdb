from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    SignUpView,
    SignInView,
    UserViewSet,
    UserMeViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
)


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")
review_router = routers.NestedSimpleRouter(router, r"titles", lookup="titles")
review_router.register(r"reviews", ReviewViewSet, basename="reviews")
comment_router = routers.NestedSimpleRouter(review_router, r"reviews", lookup="review")
comment_router.register(r"comments", CommentViewSet, basename="comment")


urlpatterns = [
    path(
        "users/me/",
        UserMeViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
    ),
    path("", include(router.urls)),
    path("", include(review_router.urls)),
    path("", include(comment_router.urls)),
    path("auth/email/", SignUpView.as_view()),
    path("auth/token/", SignInView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
