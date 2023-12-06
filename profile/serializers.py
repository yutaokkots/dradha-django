"""Serializer classes for the Profile model."""
from rest_framework import serializers
from django.core.validators import MaxLengthValidator
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """ Class representing a serializer for the Profile model."""

    class Meta:
        """ Meta options for ProfileSerializer.
        
        Attributes
        ----------
        model (Profile): 
            The model associated with this serializer.
        fields (list):
            A list of fields to include in the serialized output.
        """
        model = Profile
        fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"] 
        read_only_fields = ["user"]

class CreateProfileSerializer(serializers.ModelSerializer):
    """ Serializer class for creating and updating a Serializer instance."""

    location = serializers.CharField(
        required=False,
        validators=[MaxLengthValidator(75)])
    bio = serializers.CharField(
        required=False,
        validators=[MaxLengthValidator(200)])
    company = serializers.CharField(
        validators=[MaxLengthValidator(100)],
        required=False)
    theme = serializers.CharField(
        validators=[MaxLengthValidator(10)],
        required=False)
    github_url = serializers.CharField(
        validators=[MaxLengthValidator(200)],
        required=False)
    website = serializers.CharField(
        validators=[MaxLengthValidator(200)],
        required=False)
    twitter_username = serializers.CharField(
        validators=[MaxLengthValidator(15)],
        required=False)
    
    class Meta:
        """ Meta options for CreateProfileSerializer.

        Attributes
        ----------
        model (User): 
            The model associated with this serializer.
        fields (list):
            A list of fields for creating or updating a Profile instance.
        """
        model = Profile
        fields = ['id', 'username', 'email', 'avatar_url', 'bio', 'location', 'company', 'theme', 'github_url', 'website', 'twitter_username']
    
    def validate(self, attrs):
        """Validates the Profile information."""

    def update(self, validated_data):
        """Updates the Profile information."""
