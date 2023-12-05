"""Serializer classes for the Profile model."""
from rest_framework import serializers
from django.core.validators import MaxLengthValidator
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = Profile
        fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]

class CreateProfileSerializer(serializers.ModelSerializer):

    #user                  # models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = serializers.CharField()             # models.CharField(max_length=75, blank=True)
    bio = serializers.CharField()                  # models.CharField(max_length=200, blank=True)
    company = serializers.CharField()               # models.CharField(max_length=100, blank=True)
    theme = serializers.CharField()                # models.CharField(max_length=10, blank=True)
    github_url = serializers.CharField()           # models.URLField(max_length=140, blank=True)
    website = serializers.CharField()              # models.URLField(max_length=200, blank=True)
    twitter_username = serializers.CharField()     # models.CharField(max_length=15, blank=True)
