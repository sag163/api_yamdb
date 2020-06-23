from django.urls import path
from .views import Signup, Avtorizeytion, UserList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/email/', Signup.as_view()),
    path('auth/token/', Avtorizeytion.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserList.as_view()),
]