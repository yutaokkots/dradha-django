"""Test module for 'profile' models using Django REST framework"""
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from profile.models import Profile
from useraccounts.models import User
from django.shortcuts import get_object_or_404

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
    """Class for testing the profile model. 
    
    Methods
    -------
    setup()
        Creates a user and a profile simultaenously (1:1 relationship).
    test_user_creation()
        Verifies the user was created during setup.
    test_profile_update()
        Updates the user profile with new information.
    test_invalid_profile_edit()
        (Failure) Attempts to edit a user profile with invalid profile fields. 
    test_profile_get()
        Retreives a valid user.
    test_profile_get_invalid()
        (Failure) Attempts to access a non-existent user. 
    """

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

        """ Tests the update of the Profile model via a PUT request. """
        response = self.client.put(
            reverse('updateprofile', 
                kwargs={'userslug': self.valid_user_username}), 
            data=json.dumps(self.valid_profile_1),
            content_type='application/json',
            HTTP_ACCEPT='application/json'
        )
        test_fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
        for field in test_fields:
            self.assertEqual(response.data[field], self.valid_profile_1[field])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

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

    def test_profile_update(self):
        """ Tests an update of the Profile model via a PUT request. """
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
            response = self.client.put(
                reverse('updateprofile', 
                    kwargs={'userslug': self.valid_user_username}), 
                data=json.dumps(edited_profile),
                content_type='application/json',
                HTTP_ACCEPT='application/json'
            )
            test_fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
            for field in test_fields:
                self.assertEqual(response.data[field], edited_profile[field])
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_invalid_profile_edit(self):
        """Create another valid user, but unsuccessfully update invalid profile information."""
        with self.subTest("Create another valid user (valid_user_2) which will create a Profile instance."):
            response = self.client.post(USER_CREATE_ENDPOINT, self.valid_user_2)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["username"], self.valid_user_username_2)
        with self.subTest("Attempt to update the valid_user_2's Profile with invalid data."):
            invalid_profile = {
                "location":"Seattle, WA",
                "bio":"Back-End Developer",
                "company":"StartupOne",
                "theme":"themecharlimitis10",
                "github_url":"https://github.com/a08dk2",
                "website":"www.StartupOne1.co",
                "twitter_username":"@StartupOne"
            }
            response = self.client.put(
                reverse('updateprofile', 
                    kwargs={'userslug': self.valid_user_username_2}), 
                data=json.dumps(invalid_profile),
                content_type='application/json',
                HTTP_ACCEPT='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.subTest("Confirm incomplete profile was not saved in the Profile database."):
            user_2 = get_object_or_404(User, username=self.valid_user_username_2)
            user_profile = Profile.objects.get(user=user_2.id)
            test_fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
            for field in test_fields:
                field_value = getattr(user_profile, field)
                self.assertEqual(field_value, "")
        with self.subTest("Successfully update valid profile info, and retrieve it via a PUT request."):
            response = self.client.put(
                reverse('updateprofile', 
                    kwargs={'userslug': self.valid_user_username_2}), 
                data=json.dumps(self.valid_profile_2),
                content_type='application/json',
                HTTP_ACCEPT='application/json'
            )
            test_fields = ["location", "bio", "company", "theme", "github_url", "website", "twitter_username"]
            for field in test_fields:
                self.assertEqual(response.data[field], self.valid_profile_2[field])
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_profile_get(self):
        """Tests getting profile information using a GET request."""
        username = self.valid_user_username 
        response = self.client.get(reverse('getprofile', kwargs={'userslug': username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.valid_profile_1)

    def test_profile_get_invalid(self):
        """Tests getting invalid profile information using a GET request."""
        invalid_username = "rmaraiwo"
        response = self.client.get(reverse('getprofile', kwargs={'userslug': invalid_username}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
