"""Module providing URL patterns for user-related API views"""
from django.urls import path
from .views import RegisterUserAPIView, UserDetailAPI

# 'api/auth/'
urlpatterns = [
    path("getuser/<int:user_id>/", UserDetailAPI.as_view(), name="getuser"),
    path("userprofile/<int:user_id>/", UserDetailAPI.as_view(), name="userprofile"),
    path("createuser/", RegisterUserAPIView.as_view(), name="registeruser"),
]
