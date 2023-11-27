from django.urls import path


# 'api/auth/'
urlpatterns = [
    path("createuser/", RegisterAPI.as_view(), name="createuser"),
]