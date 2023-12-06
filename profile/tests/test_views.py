"""Test module for 'profile' models using Django REST framework"""
from django.test import TestCase
from rest_framework import status
from django.db.utils import DataError, IntegrityError
from django.urls import reverse
from profile.models import Profile
from useraccounts.models import User
from useraccounts.serializers import UserSerializer

VALID_USER = {
    "username": "dradhauser",
    "email": "test@mellow.com",
    "password": "testpassword",
    "password_confirm": "testpassword",
    "oauth_login": "None"
}
VALID_PROFILE_1 = {
    "location":"Denver, CO",
    "bio":"Full-Stack Engineer",
    "company":"Dradha",
    "theme":"dark",
    "github_url":"https://github.com/",
    "website":"www.dradha.co",
    "twitter_username":"dradha"
}
VALID_OAUTH_USER = {
    "username": "starterupperuser",
    "email": "test@startupOne1.co",
    "password": "",
    "password_confirm": "",
    "oauth_login": "skej932kfnma58shdkel",
    "avatar_url":"test@startupOne1.co/newimage.png"
}
VALID_PROFILE_2 = {
    "location":"Seattle, WA",
    "bio":"Back-End Developer",
    "company":"StartupOne",
    "theme":"light",
    "github_url":"https://github.com/a08dk2",
    "website":"www.StartupOne1.co",
    "twitter_username":"@StartupOne"
}

USER_CREATE_ENDPOINT = "/api/auth/createuser/"

class TestProfileModel(TestCase):
    """Class for testing the profile model. """

    def setUp(self):
        """ Set up the test for creating a user and a profile."""
        self.valid_user = VALID_USER
        self.valid_user_username = self.valid_user["username"]
        self.valid_profile_1 = VALID_PROFILE_1
        self.valid_user_2 = VALID_OAUTH_USER
        self.valid_user_username_2 = self.valid_user_2["username"]
        self.valid_profile_2 = VALID_PROFILE_2

        response = self.client.post(USER_CREATE_ENDPOINT, self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "dradhauser")

        # """ Tests the update of the Profile model via a PUT request. """
        # response = self.client.put(reverse("updateprofile"), self.valid_profile_1)
        # test_fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
        # for field in test_fields:
        #     self.assertEqual(response.data[field], self.valid_profile_1[field])
        # # self.assertEqual(response.data["location"], "Denver, CO")
        # # self.assertEqual(response.data["bio"], "Full-Stack Engineer")
        # # self.assertEqual(response.data["company"], "Dradha")
        # # self.assertEqual(response.data["theme"], "dark")
        # # self.assertEqual(response.data["github_url"], "https://github.com/")
        # # self.assertEqual(response.data["website"], "www.dradha.co")
        # # self.assertEqual(response.data["twitter_username"], "dradha")
        # self.assertEqual(response.status, status.HTTP_202_ACCEPTED)


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

    # def test_profile_update(self):
    #     """ Tests the update of the Profile model via a PUT request. """
    #     with self.subTest("Test the modification of the user profile"):
    #         edited_profile = {
    #             "location":"",
    #             "bio":"Full-Stack Software Engineer",
    #             "company":"",
    #             "theme":"",
    #             "github_url":"",
    #             "website":"www.dradha.co",
    #             "twitter_username":""
    #         }
    #         response = self.client.put(reverse("updateprofile"), edited_profile)
    #         test_fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
    #         for field in test_fields:
    #             self.assertEqual(response.data[field], self.edited_profile[field])
    #         # self.assertEqual(response.data["bio"], "Full-Stack Software Engineer")
    #         # self.assertEqual(response.data["location"], "Denver, CO")
    #         # self.assertEqual(response.data["company"], "Dradha")
    #         # self.assertEqual(response.data["theme"], "dark")
    #         # self.assertEqual(response.data["github_url"], "https://github.com/")
    #         # self.assertEqual(response.data["website"], "www.dradha.co")
    #         # self.assertEqual(response.data["twitter_username"], "dradha")
    #         self.assertEqual(response.status, status.HTTP_202_ACCEPTED)

    # def test_incomplete_profile_edit(self):
    #     """Create another valid user, but unsuccessfully update invalid profile information."""
    #     with self.subTest("Create a second valid user."):
    #         response = self.client.post(USER_CREATE_ENDPOINT, self.valid_user_2)
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertEqual(response.data["username"], self.valid_user_username_2)
    #     with self.subTest("Attempt to update and retrieve a Profile model of the second user."):
    #         incomplete_profile = {
    #             "location":"Seattle, WA",
    #             "bio":"Back-End Developer",
    #             "company":"StartupOne",
    #             "theme":"themecharlimitis10",
    #             "github_url":"https://github.com/a08dk2",
    #             "website":"www.StartupOne1.co",
    #             "twitter_username":"@StartupOne"
    #         }
    #         response = self.client.put(reverse("updateprofile"), incomplete_profile)
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #         user_2 = User.objects.get(username=self.valid_user_username_2)
    #         user_profile = Profile.objects.get(user=user_2)
    #         test_fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
    #         for field in test_fields:
    #             self.assertEqual(user_profile[field], "")
    #     with self.subTest("Successfully update and retrieve a Profile model via a PUT request."):
    #         response = self.client.put(reverse("updateprofile"), self.valid_profile_2)
    #         self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    #         test_fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
    #         for field in test_fields:
    #             self.assertEqual(response.data[field], self.valid_profile_2[field])
    
    def test_profile_get(self):
        """Tests getting profile information using a GET request."""
        username = self.valid_user_username 
        response = self.client.get(reverse('getprofile', kwargs={'userslug': username}))
        # response = self.client.get(f"{reverse('getprofile')}/{username}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.valid_profile_1)

    def test_profile_get_invalid(self):
        """Tests getting invalid profile information using a GET request."""
        invalid_username = "rmaraiwo"
        response = self.client.get(reverse('getprofile', kwargs={'userslug': invalid_username}))
        # response = self.client.get(f"{reverse('getprofile')}/{invalid_username}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
