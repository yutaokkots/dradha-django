"""Serializer classes for the User model."""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import EmailValidator, MinLengthValidator, MaxLengthValidator
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
        fields = ['id', 'username', 'email', "avatar_url"]


class CreateUserSerializer(serializers.Serializer):
    """Serializer Class for creating a User instance"""

    username = serializers.CharField(
        validators=[MinLengthValidator(4), MaxLengthValidator(30)]
    )

    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator, MaxLengthValidator(75)]
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password], 
        style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=False,
        style={"input_type": "password"}
    )
    oauth_login = serializers.CharField(
        required=True
    )
    avatar_url = serializers.CharField(
        required=False,
        allow_blank=True,
        default="http://www.dradha.co/profile-images/avatar_osteospermum.jpg"
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
        fields = ['id','username', 'email',"oauth_login","avatar_url"]
        extra_kwargs = {'password':
                        {'write_only':True,
                         'min_length':6}}

    def validate(self, attrs):
        """Validates the password """
        if attrs["oauth_login"] == "False":
            if not attrs["password"] or not attrs["password_confirm"]:
                raise serializers.ValidationError('Requires password.')
            elif (attrs['password'] and 
                attrs['password_confirm'] and 
                attrs['password'] != attrs['password_confirm']):
                raise serializers.ValidationError('Passwords do not match.')
        if attrs["oauth_login"] != "False" and attrs["oauth_login"] != "skej932kfnma58shdkelanc2kdp":
            raise serializers.ValidationError("Error with account creation.")
        return attrs
    
    # def is_valid(self, *args, **kwargs):
    #     """Validates the password """
    #     oauth_login = self.validated_data.get('oauth_login', 'False')
    #     password = self.validated_data.get('password')
    #     password_confirm = self.validated_data.get('password_confirm')

    #     if oauth_login == "False":
    #         if not password or not password_confirm:
    #             raise serializers.ValidationError('Requires password.')
    #         elif (password and 
    #             password_confirm and 
    #             password != password_confirm):
    #             raise serializers.ValidationError('Passwords do not match.')
    #     if oauth_login != "False" and oauth_login != "skej932kfnma58shdkelanc2kdp":
    #         raise serializers.ValidationError("Error with account creation.")
    #     return super(CreateUserSerializer, self).is_valid(*args, **kwargs)
        
    def create(self, validated_data):
        """Creates a user instance """
        # user = User.objects.create_user(
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        #     password=validated_data['password'],
        # ) if validated_data["oauth_login"] == "False" else User.objects.create(
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        # ) 
        user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'] if validated_data["oauth_login"] == "False" else None,
        )       
        user.save()
        user.oauth_login = validated_data["oauth_login"]
        user.avatar_url = validated_data["avatar_url"]
    

        # saveduser = User.objects.get(username=validated_data['username'])
        # print("saved user=> ", saveduser)
        # Additionally create a profile instance.
        return user