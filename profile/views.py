from django.shortcuts import render
from rest_framework import status, serializers
from rest_framework.views import APIView

# Create your views here.

from .models import Profile

# api/profile/
class CreateProfileView(APIView):
    """ Class for creating a profile for a user
    Attributes
    ----------
    serializer_class:
        Use the CreateProfileSerializer for serialization. 
    """

    def post(self, request, *args, **kwargs):
        try:
            pass
        except:
            pass
        