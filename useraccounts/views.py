"""Module providing view classes for user-related requests/responses."""
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
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

    ##@action(methods=['get'], detail=False, url_path='getuser')
    def get(self, request, user_id):
        """Method for getting user information. """
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    # draft
    def getProfile(self, request, user_id):
        """Method for getting user information. """
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# api/auth/createuser
class RegisterUserAPIView(APIView):
    """Class for registering a new user.
    
    Attributes
    ----------
    permission_classes: 
        Any user, regardless of authentication status, has permission to access the view.
    serializer_class:
        Use the CreateUserSerializer for serialization. 
    """

    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    # def create(self, request, *args, **kwargs):

    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     headers = self.get_success_headers(serializer.data)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# api/auth/oauthlogin
class OAuthView():
    pass