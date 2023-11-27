"""Module providing URL patterns for user-related API views"""
from django.urls import path
from .views import RegisterUserAPIView, UserDetailAPI

# 'api/auth/'
urlpatterns = [
    path("getuser/", UserDetailAPI.as_view(), name="userdetail"),
    path("createuser/", RegisterUserAPIView.as_view(), name="registeruser"),
]
