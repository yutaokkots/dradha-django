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
    "github_url":"https://www.github.com/",
    "website":"www.dradha.co",
    "twitter_username":"dradha"
}

INVALID_PROFILE = {
    "location":"Denver, CO",
    "bio":"Full-Stack Engineer",
    "company":"Dradha",
    "theme":"",
    "github_url":"github.com",
    "website":"drada",
    "twitter_username":"dradha"
}

VALID_OAUTH_USER = {
    "username": "OAuthUser",
    "email": "testOauthUser@mail.net",
    "password": "",
    "password_confirm": "",
    "oauth_login": "skej932kfnma58shdkel",
    "avatar_url":"www.dradha.co/newimage.png"
}

USER_CREATE_ENDPOINT = "/api/auth/createuser/"

class TestProfileModel(TestCase):
    """Class for testing the profile model. """

    def setUp(self):
        """ Set up the test for creating a user and a profile (1:1 relationship)."""
        self.valid_user = VALID_USER
        self.valid_user_username = self.valid_user["username"]
        self.valid_profile = VALID_PROFILE
        self.invalid_profile = INVALID_PROFILE
        self.valid_oauth_user = VALID_OAUTH_USER

        response = self.client.post(USER_CREATE_ENDPOINT, self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "dradhauser")

    def test_user_creation(self):
        """ Tests the successful creation of a User and accompanying profile."""
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

    def test_profile_edit(self):
        """ Tests the update of a user profile via the Profile model."""
        user = User.objects.get(username=self.valid_user_username)
        user_profile = Profile.objects.get(user=user)
        with self.subTest("Verify that profile fields are empty after initialization."):
            location = user_profile.location
            bio = user_profile.bio
            company = user_profile.company
            theme = user_profile.theme
            github_url = user_profile.github_url
            website = user_profile.website
            twitter_username = user_profile.twitter_username
            test_fields = [location, bio, company, theme, github_url, website, twitter_username]
            for i, value in enumerate(test_fields):
                self.assertEqual(value, "")

        profile_id = Profile.objects.update(user=user, **self.valid_profile)
        updated_profile = Profile.objects.get(user=profile_id)
        with self.subTest("Verify that profile fields are filled after updating Profile."):
            location = updated_profile.location
            bio = updated_profile.bio
            company = updated_profile.company
            theme = updated_profile.theme
            github_url  = updated_profile.github_url
            website = updated_profile.website
            twitter_username = updated_profile.twitter_username
            test_fields = [location, bio, company, theme, github_url, website, twitter_username]
            test_assertions = [
                "Denver, CO", "Full-Stack Engineer", "Dradha", 
                "dark", "https://www.github.com/", "www.dradha.co", "dradha"]
            for i, value in enumerate(test_fields):
                self.assertEqual(value, test_assertions[i])
                self.assertNotEqual(value, "")

    # def test_incomplete_profile_edit(self):
    #     user = User.objects.get(username=self.valid_user_username)
    #     user_profile = Profile.objects.get(user=user)
    #     profile_id = Profile.objects.update(user=user, **self.valid_profile)
    #     updated_profile = Profile.objects.get(user=profile_id)

    #     self.invalid_profile
        
    # def test_valid_oauth_user_profile(self):
    #     response = self.client.post(USER_CREATE_ENDPOINT, self.valid_oauth_user)
    #     self.assertEqual(response.data["username"], "OAuthUser")   
    #     self.assertEqual(response.data["email"], "testOauthUser@mail.net")   
