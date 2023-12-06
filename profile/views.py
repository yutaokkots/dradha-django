import logging
from django.http import HttpResponseServerError
from django.shortcuts import render
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Profile
from useraccounts.models import User
from .serializers import UpdateProfileSerializer, ProfileSerializer

logger = logging.getLogger(__name__)

# api/profile/
class ProfileView(APIView):
    """ Class for creating a profile for a user
    Attributes
    ----------
    serializer_class:
        Use the UpdateProfileSerializer for serialization. 
    """

    # api/profile/u/<slug:userslug>
    def get(self, request, userslug, *args, **kwargs):
        """Method for retrieving an returning a user's information."""
        try:
            user = get_object_or_404(User, username=userslug)
            profile = user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateProfileView(APIView):
    def put(self, request, userslug, *args, **kwargs):
        try:
            user = get_object_or_404(User, username=userslug)
            profile = user.profile
            data = request.data
            serializer = UpdateProfileSerializer(data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_profile = serializer.update(profile, serializer.validated_data)
            deserializer = ProfileSerializer(updated_profile)
            return Response(deserializer.data, status=status.HTTP_202_ACCEPTED)
        except serializers.ValidationError as e:
            print(e)
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("An error occurred: %s", e, exc_info=True)
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_400_BAD_REQUEST)
        