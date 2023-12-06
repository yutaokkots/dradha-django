"""Test module for 'profile' models using Django REST framework"""
import django
django.setup()
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError
from rest_framework import status
from useraccounts.models import User
from profile.models import Profile
from useraccounts.serializers import UserSerializer
from django.urls import reverse


VALID_USER_1 = {
    "username": "dradhauser",
    "email": "test@mellow.com",
    "password": "testpassword",
    "password_confirm": "testpassword",
    "oauth_login": "None"
}
VALID_USER_2 = {
    "username": "secondUser",
    "email": "test@marsh.com",
    "password": "testpassword123",
    "password_confirm": "testpassword123",
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
INCOMPLETE_PROFILE = {
    "location":"Denver, CO",
    "bio":"Full-Stack Engineer",
    "company":"",
    "theme":"",
    "github_url":"github.com",
    "website":"drada",
    "twitter_username":"twittercharlimitis15"
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
        self.valid_user_1 = VALID_USER_1
        self.valid_user_2 = VALID_USER_2
        self.valid_profile = VALID_PROFILE
        self.valid_oauth_user = VALID_OAUTH_USER

        response = self.client.post(USER_CREATE_ENDPOINT, self.valid_user_1)
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
            addedUser = User.objects.get(username="dradhauser")
            addedUserProfile = Profile.objects.get(user=addedUser.id)
            self.assertEqual(addedUserProfile.user.username, "dradhauser")

    def test_profile_edit(self):
        """ Tests the update of a user profile via the Profile model."""
        user = User.objects.get(username="dradhauser")
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
        Profile.objects.update(user=user, **self.valid_profile)
        updated_profile = Profile.objects.get(user=user)
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
        with self.subTest("Verify the number of all profiles has not changed"):
            allProfiles = Profile.objects.all()
            self.assertEqual(allProfiles.count(), 1)

    def test_incomplete_profile_edit(self):
        """Create another valid user, but add invalid profile information."""
        with self.subTest("Create a second valid user."):
            response = self.client.post(USER_CREATE_ENDPOINT, self.valid_user_2)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["username"], "secondUser")
        with self.subTest("Retrieve the Profile model of the second user."):
            user_2 = User.objects.get(username="secondUser")
            user_profile = Profile.objects.get(user=user_2)
        with self.subTest("Update the Profile fields of the second user, confirm not saved."):
            incomplete_profile = {
                "location":"Denver, CO",
                "bio":"Full-Stack Engineer",
                "company":"",
                "theme":"",
                "github_url":"github.com",
                "website":"drada",
                "twitter_username":"twittercharlimitis15"
            }
            user_profile.location = incomplete_profile["location"]
            user_profile.bio = incomplete_profile["bio"]
            user_profile.company = incomplete_profile["company"]
            user_profile.theme = incomplete_profile["theme"]
            user_profile.github_url = incomplete_profile["github_url"]
            user_profile.website = incomplete_profile["website"]
            user_profile.twitter_username = incomplete_profile["twitter_username"]
            updated_profile_before_save = Profile.objects.get(user=user_2)
            self.assertEqual(updated_profile_before_save.bio, "")
            self.assertNotEqual(updated_profile_before_save.bio, "Full-Stack Engineer")
        with self.subTest("Confirm error caused by incomplete profile."):
            with self.assertRaises(DataError):
                user_profile.save()
            with self.assertRaises(Exception) as context:
                user_profile.save()
                caught_exception = context.exception
                self.assertTrue(isinstance(caught_exception, (DataError, IntegrityError)))
            print("Assert raises were executed.")


    
   
    
    
    
   
    
    #     # user_profile = Profile.objects.get(user=user_2)
    #     # print(user_profile)
    #     profile_id = Profile.objects.update(user=user_2, **INCOMPLETE_PROFILE)
    #     # updated_profile = Profile.objects.get(user=profile_id)
    #     print(profile_id)
        
    # def test_valid_oauth_user_profile(self):
    #     response = self.client.post(USER_CREATE_ENDPOINT, self.valid_oauth_user)
    #     self.assertEqual(response.data["username"], "OAuthUser")   
    #     self.assertEqual(response.data["email"], "testOauthUser@mail.net")   
