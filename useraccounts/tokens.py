"""Module for JSON web-token generation"""
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

#from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer class for the token retrieval from user. """

    @classmethod
    def get_token(cls, user):
        """Retrieves and gets the token for the user."""
        token = super().get_token(user)
        token['name'] = user.username
        return token 

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def create_jwt_pair_for_user(user:User):
    """Creates a refresh token using simplejwt RefreshToken class."""
    refresh = RefreshToken.for_user(user)
    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }
    return tokens

