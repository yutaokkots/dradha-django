"""Serializer classes for the User model."""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import EmailValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User
from oauth.services import verify_state
from useraccounts.services import oauth_uid_check_approved, oauth_uid_get_service


class UserSerializer(serializers.ModelSerializer):
    """Class representing a serializer for the User model."""

    bio = serializers.CharField(source='profile.bio')
    location = serializers.CharField(source='profile.location')

    class Meta:
        """ Meta options for the UserSerializer.

        Attributes
        ----------
        model (User): 
            The model associated with this serializer.
        fields (list):
            A list of fields to include in the serialized output.
        """

        model = User
        fields = ['id', 'username', 'email', "avatar_url", "bio", "location"]

class CreateUserSerializer(serializers.Serializer):
    """Serializer Class for creating a User instance"""

    username = serializers.CharField(
        required=True,
        validators=[MinLengthValidator(4), MaxLengthValidator(30), UniqueValidator])
    email = serializers.EmailField(
        required=False,
        validators=[EmailValidator, MaxLengthValidator(75)])
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password], 
        style={"input_type": "password"})
    password_confirm = serializers.CharField(
        write_only=True,
        required=False,
        style={"input_type": "password"})
    oauth_login = serializers.CharField(
        required=True)
    avatar_url = serializers.CharField(
        required=False,
        allow_blank=True,
        default="http://www.dradha.co/profile-images/avatar_osteospermum.jpg")

    class Meta:
        """ Meta options for the UserSerializer.

        Attributes
        ----------
        model (User): 
            The model associated with this serializer.
        fields (list):
            A list of fields for creating or updating a User instance.
        extra_kwargs:
            Additional options for specific fields, such as 'write_only' and 'min_length' for the 'password' field.
        """

        model = User
        fields = ["id", "username", "email", "oauth_login", "avatar_url"]
        extra_kwargs = {'password':
                        {'write_only':True,
                         'min_length':6}}

    def validate(self, attrs):
        """User model validator for serialization.
        1. Determines the type of User being created ("oauth_login" == "Dradha" -> dradha)
        2. Validates the password and username.
        """
        service_type = oauth_uid_get_service(attrs["oauth_login"])
        if service_type == "dradha":
            if not attrs["password"] or not attrs["password_confirm"]:
                raise serializers.ValidationError('Requires password.')
            elif (attrs['password'] and 
                attrs['password_confirm'] and 
                attrs['password'] != attrs['password_confirm']):
                raise serializers.ValidationError('Passwords do not match.')
        if service_type != "dradha" and not verify_state(attrs["oauth_login"]):
            raise serializers.ValidationError("Error with account creation.")
        existing_user = User.objects.filter(username=attrs["username"]).exists()
        if existing_user:
            raise serializers.ValidationError("Database error.")
        return attrs
    
    def create(self, validated_data):
        """Creates a user instance."""
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            oauth_login=validated_data.get("oauth_login")
        )       
        user.save()
        default_url = "http://www.dradha.co/profile-images/avatar_osteospermum.jpg"
        user.avatar_url = validated_data.get("avatar_url", default_url) or default_url
        user.save(update_fields=["avatar_url"])
        return user


class LoginSerializer(serializers.Serializer):
    """Class for login serialization."""

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """Validation function for users with username and password."""
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credentials are incorrect")
    
