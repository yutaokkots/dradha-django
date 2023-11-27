"""Serializer classes for the User model."""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Class representing a serializer for the User model"""

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
        fields = ['id', 'username', 'email']

class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer Class for creating a User instance"""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all)]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        """ Meta options for the UserSerializer.

        Attributes
        ----------
        model (User): 
            The model associated with this serializer.
        fields (list):
            A list of fields to include in the serialized output.
        extra_kwargs:
            Additional options for specific fields, such as 'write_only' and 'min_length' for the 'password' field.
        """

        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        extra_kwargs = {'password':
                        {'write_only':True,
                         'min_length':6}}

    def validate(self, attrs):
        """Validates the password """

        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs

    def create(self, validated_data):
        """Creates a user instance """

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
