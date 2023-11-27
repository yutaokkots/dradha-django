from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .models import User
# Create your views here.

# api/auth/getUser
class UserDetailAPI(APIView):
    authentication_classes = [TokenAuthentication] # the view expects requests to include a valid token in the request header for authentication
    permission_classes = [AllowAny] # any user, regardless of authentication status, has permission to access the view

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
# api/auth/createuser
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny)
    serializer_class = CreateUserSerializer

