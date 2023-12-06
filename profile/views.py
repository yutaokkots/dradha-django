from django.shortcuts import render
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Profile
from useraccounts.models import User
from .serializers import CreateProfileSerializer, ProfileSerializer

# api/profile/
class ProfileView(APIView):
    """ Class for creating a profile for a user
    Attributes
    ----------
    serializer_class:
        Use the CreateProfileSerializer for serialization. 
    """

    # api/profile/u/<slug:userslug>
    def get(self, request, userslug, *args, **kwargs):
        """Method for retrieving an returning a user's information."""
        try:
            user = get_object_or_404(User, username=userslug)
            #user = User.objects.get(username=userslug)
            # profile = Profile.objects.get(id=user.id)
            profile = user.profile
            serializer = ProfileSerializer(profile)
            print(serializer.data)
            return Response(serializer.data)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateProfileView(APIView):

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = CreateProfileSerializer(data=data)
        except:
            pass