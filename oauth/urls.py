from django.urls import include, path
from oauth.views import GithubOauthAPI, GithubStateGenerator

urlpatterns = [
    path("callback/state", GithubStateGenerator.as_view(http_method_names=['get']), name="stategenerator"),
    path("callback/", GithubOauthAPI.as_view(http_method_names=['get', 'post']), name="callback"),
    path("token/", GithubOauthAPI.as_view(http_method_names=['post_token']), name="token"),
]