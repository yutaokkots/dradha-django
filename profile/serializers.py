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

class UpdateProfileSerializer(serializers.ModelSerializer):
    """ Serializer class for creating and updating a Serializer instance."""

    location = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(75)])
    bio = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(200)])
    company = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(100)])
    theme = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(10)])
    github_url = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(200)])
    website = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(200)])
    twitter_username = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(15)])
    
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
        fields = ['user', 'location', 'bio', 'company', 'theme', 'github_url', 'website', 'twitter_username']
    
    """
    {'location': [ErrorDetail(string='This field may not be blank.', code='blank')], 
    'company': [ErrorDetail(string='This field may not be blank.', code='blank')], 
    'theme': [ErrorDetail(string='This field may not be blank.', code='blank')], 
    'github_url': [ErrorDetail(string='This field may not be blank.', code='blank')], 
    'twitter_username': [ErrorDetail(string='This field may not be blank.', code='blank')]}
    """


    # def validate(self, attrs):
    #     """Validates the Profile information."""
    #     fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
    #     for field in fields:
    #         if attrs[field] == "":
    #             attrs[field] = ""
    #     return attrs        

    def update(self, instance, validated_data):
        """Updates the Profile information."""
        instance.location = validated_data.get('location', instance.location)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.company = validated_data.get('company', instance.company)
        instance.theme = validated_data.get('theme', instance.theme)
        instance.github_url = validated_data.get('github_url', instance.github_url)
        instance.website = validated_data.get('website', instance.website)
        instance.twitter_username = validated_data.get('twitter_username', instance.twitter_username)
        instance.save()
        return instance