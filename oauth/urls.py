from django.urls import include, path
from oauth.views import GithubOauthAPI

urlpatterns = [
    path("callbackgithub/", GithubOauthAPI.as_view(http_method_names=['post']), name="callbackgithub"),
    path("tokengithub/", GithubOauthAPI.as_view(http_method_names=['post_token']), name="tokengithub"),
]