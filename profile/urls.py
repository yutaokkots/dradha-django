"""Module providing URL patterns for Profile-related API views"""
from django.urls import path

from .views import ProfileView, UpdateProfileView

urlpatterns = [
    path('createprofile/', ProfileView.as_view(), name="createprofile"),
    path('u/<slug:userslug>', UpdateProfileView.as_view(), name="updateprofile"),
    path('u/<slug:userslug>/', ProfileView.as_view(), name="getprofile"), 
]
