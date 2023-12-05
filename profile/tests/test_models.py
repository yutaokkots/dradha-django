"""Test module for 'profile' models using Django REST framework"""
import django
django.setup()
from django.test import TestCase
from useraccounts.models import User
from useraccounts.serializers import UserSerializer
from django.urls import reverse

VALID_USER = {
    "username": "testuserA",
    "email": "testuser@mail.com",
    "password": "testpassword",
    "password_confirm": "testpassword",
    "oauth_login": "None"
}

VALID_PROFILE = {
    "user":"",
    "location":"Denver, CO",
    "bio":"Full-Stack Engineer",
    "company":"Dradha",
    "theme":"dark",
    "github_url":"https://github.com/",
    "website":"www.dradha.co",
    "twitter_username":"dradha"
}

class TestProfileModel(TestCase):
    """Class for testing the profile model. """

    def setUp(self):
        self.valid_user = VALID_USER
        self.valid_profile = VALID_PROFILE

        response = self.client.post(reverse("createprofile"), self.valid_profile)