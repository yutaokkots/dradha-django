"""Module providing URL patterns for OAuth-related API views"""
from django.urls import include, path
from oauth.views import GithubOauthAPI, GithubStateGenerator
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("callback/state", GithubStateGenerator.as_view(http_method_names=['get']), name="stategenerator"),
    path("callback/", GithubOauthAPI.as_view(http_method_names=['get', 'post']), name="callback"),
    path("token/", GithubOauthAPI.as_view(http_method_names=['post_token']), name="token"),
    path("token/refresh/"),
    path("token/verify/")
]