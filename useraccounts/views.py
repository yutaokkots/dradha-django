"""Module providing view classes for user-related requests/responses."""
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .serializers import UserSerializer, CreateUserSerializer
from .models import User

# api/auth/getUser
class UserDetailAPI(APIView):
    """Class for requesting user information.

    Attributes
    ----------
    authentication_classes: 
        Token-based authentication; expects requests to include a valid token 
        in the request header for authentication.
    permission_classes: 
        Any user, regardless of authentication status, has permission to access the view.

    Methods
    -------
    get(self, request, *args, **kwargs): 
        Retrieves user information for the authenticated user.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """Method for getting user information. """

        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# api/auth/createuser
class RegisterUserAPIView(generics.CreateAPIView):
    """Class for registering a new user."""

    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer
