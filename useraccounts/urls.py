from django.urls import path
from .views import RegisterUserAPIView, UserDetailAPI

# 'api/auth/'
urlpatterns = [
    path("getuser/", UserDetailAPI.as_view(), name="getuser"),
    path("createuser/", RegisterUserAPIView.as_view(), name="createuser"),
]