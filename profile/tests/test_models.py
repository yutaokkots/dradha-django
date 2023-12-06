"""Test module for 'profile' models using Django REST framework"""
import django
django.setup()
from django.test import TestCase
from rest_framework import status
from useraccounts.models import User
from profile.models import Profile
from useraccounts.serializers import UserSerializer
from django.urls import reverse


VALID_USER = {
    "username": "dradhauser",
    "email": "test@mellow.com",
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

USER_CREATE_ENDPOINT = "/api/auth/createuser/"

class TestProfileModel(TestCase):
    """Class for testing the profile model. """

    def setUp(self):
        self.valid_user = VALID_USER
        self.valid_user_username = self.valid_user["username"]
        self.valid_profile = VALID_PROFILE

        response = self.client.post(USER_CREATE_ENDPOINT, self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "dradhauser")
        # with self.subTest("Test the number of users after registration"):
        #     allUsers = User.objects.getAll()
        #     self.assertEqual(allUsers.count(), 1)
        # with self.subTest("Test the number of Profiles after user registration"):
        #     userProfile = Profile.objects.get(username="dradhauser")
        #     self.assertEquals(userProfile.user.username, "dradhauser")
        #     allProfiles = Profile.objects.getAll()
        #     self.assertEqual(allProfiles.count(), 2)

    def test_usercreation(self):
        # with self.subTest("Create an initial user."):
        #     response = self.client.post(USER_CREATE_ENDPOINT, self.valid_profile)
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(response.data["username"], "dradhauser")
        with self.subTest("Test the number of users after registration"):
            allUsers = User.objects.all()
            self.assertEqual(allUsers.count(), 1)
        with self.subTest("Test the number of Profiles after user registration"):
            allProfiles = Profile.objects.all()
            self.assertEqual(allProfiles.count(), 1)
        with self.subTest("Test the created profile 'dradhauser' can be retrieved"):
            addedUser = User.objects.get(username="dradhauser")
            addedUserProfile = Profile.objects.get(user=addedUser.id)
            self.assertEqual(addedUserProfile.user.username, "dradhauser")

