"""Module providing URL patterns for user-related API views"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import RegisterUserAPIView, UserDetailAPI

# 'api/auth/'
urlpatterns = [
    path("getuser/<int:user_id>/", UserDetailAPI.as_view(), name="getuser"),
    path("userprofile/<int:user_id>/", UserDetailAPI.as_view(), name="userprofile"),
    path("createuser/", RegisterUserAPIView.as_view(), name="registeruser"),
    path("login/", RegisterUserAPIView.as_view(), name="login"),
    path("oauthlogin/", RegisterUserAPIView.as_view(), name="oauthlogin"),
    path("token/refresh/", TokenRefreshView.as_view(), name="tokenrefresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="tokenverify")
]
