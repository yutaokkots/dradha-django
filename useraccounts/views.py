"""Module providing view classes for user-related requests/responses."""
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework import generics
from django.db import IntegrityError
from .serializers import UserSerializer, CreateUserSerializer
from .models import User
from useraccounts.services import user_model_flow

# api/auth/getUser
class UserDetailAPI(APIView):
    """UserDetailAPI Class for requesting user information.

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
        """GET method for getting user information."""
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# api/auth/createuser
class RegisterUserAPIView(APIView):
    """RegisterUserAPIView Class for registering a new user.

    Attributes
    ----------
    permission_classes: 
        Any user, regardless of authentication status, has permission to access the view.
    serializer_class:
        Use the CreateUserSerializer for serialization. 
    """

    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        """POST method to save a new User."""
        try:
            data = request.data
            prevalidated_data = user_model_flow(data)
            serializer = CreateUserSerializer(data=prevalidated_data)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                try:
                    userdata = serializer.create(serializer.validated_data)
                    deserializer = UserSerializer(userdata)
                    return Response(deserializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    return Response({"error": f"Database error: {str(e)}"}, status=status.HTTP_409_CONFLICT)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_400_BAD_REQUEST)

# api/auth/oauthlogin
class OAuthView():
    pass