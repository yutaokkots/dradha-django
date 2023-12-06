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
    "location":"Denver, CO",
    "bio":"Full-Stack Engineer",
    "company":"Dradha",
    "theme":"dark",
    "github_url":"https://github.com/",
    "website":"www.dradha.co",
    "twitter_username":"dradha"
}

VALID_OAUTH_USER = {
    "username": "dradhauser",
    "email": "test@mellow.com",
    "password": "",
    "password_confirm": "",
    "oauth_login": "skej932kfnma58shdkel",
    "avatar_url":"www.dradha.co/newimage.png"
}

USER_CREATE_ENDPOINT = "/api/auth/createuser/"

class TestProfileModel(TestCase):
    """Class for testing the profile model. """

    def setUp(self):
        """ Set up the test for creating a user and a profile."""
        self.valid_user = VALID_USER
        self.valid_user_username = self.valid_user["username"]
        self.valid_profile = VALID_PROFILE

        response = self.client.post(USER_CREATE_ENDPOINT, self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "dradhauser")

    def test_user_creation(self):
        """ Tests the successful creation of a User and accompanying profile"""
        with self.subTest("Test the number of users after registration"):
            allUsers = User.objects.all()
            self.assertEqual(allUsers.count(), 1)
        with self.subTest("Test the number of Profiles after user registration"):
            allProfiles = Profile.objects.all()
            self.assertEqual(allProfiles.count(), 1)
        with self.subTest("Test the created profile 'dradhauser' can be retrieved"):
            addedUser = User.objects.get(username=self.valid_user_username)
            addedUserProfile = Profile.objects.get(user=addedUser.id)
            self.assertEqual(addedUserProfile.user.username, "dradhauser")


    def test_automatic_oauth_creation(self):
        """ Tests the automatic creation of a profile model with an OAuth user"""


    def test_profile_update(self):
        """ Tests the update of the Profile model """
        response = self.client.put(reverse("updateprofile"), self.valid_profile)
        self.assertEqual(response.data["location"], "Denver, CO")
        self.assertEqual(response.data["bio"], "Full-Stack Engineer")
        self.assertEqual(response.data["company"], "Dradha")
        self.assertEqual(response.data["theme"], "dark")
        self.assertEqual(response.data["github_url"], "https://github.com/")
        self.assertEqual(response.data["website"], "www.dradha.co")
        self.assertEqual(response.data["twitter_username"], "dradha")
        self.assertEqual(response.status, status.HTTP_202_ACCEPTED)

        with self.subTest("Test the modification of the user profile"):
            edited_profile = {
                "location":"",
                "bio":"Full-Stack Software Engineer",
                "company":"",
                "theme":"",
                "github_url":"",
                "website":"www.dradha.co",
                "twitter_username":""
            }
            response = self.client.PUT(reverse("updateprofile"), edited_profile)
            self.assertEqual(response.data["bio"], "Full-Stack Software Engineer")
            self.assertEqual(response.data["location"], "Denver, CO")
            self.assertEqual(response.data["company"], "Dradha")
            self.assertEqual(response.data["theme"], "dark")
            self.assertEqual(response.data["github_url"], "https://github.com/")
            self.assertEqual(response.data["website"], "www.dradha.co")
            self.assertEqual(response.data["twitter_username"], "dradha")
            self.assertEqual(response.status, status.HTTP_202_ACCEPTED)