"""Test module for 'useraccounts' using Django REST framework"""
from rest_framework import status
from rest_framework.test import APITestCase
from useraccounts.models import User
from django.urls import reverse

class UserAPITest(APITestCase):
    """UserAPITest class for various test cases 

    Methods
    -------
    setup()
        Creates a user for testing.
    test_user_get_api()

    """

    def setUp(self):
        """Set up the test method for creating a user"""
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "False"
        }
        self.user_data_missing_password = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        self.user_data_invalid_password = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassworssd"
        }
        self.user_data_invalid_email = {
            "username": "testuser",
            "email": "testuser@",
            "password": "testpassword",
            "password_confirm": "testpassword"
        }
        self.user_data_invalid_username = {
            "username": "te",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword"
        }
        response = self.client.post(reverse("registeruser"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_user_profile(self):
        """Tests the successful creation of a user."""
        response = self.client.post(reverse("registeruser"), {
            "username": "testabcdeuser",
            "email": "test@email.net",
            "password": "testpassword1",
            "password_confirm": "testpassword1"
        })
        self.assertEqual(response.data["username"], "testabcdeuser")
        self.assertEqual(response.data["email"], "test@email.net")
        self.assertNotIn("password", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_missing_password(self): 
        """Tests the failure of creating a user due to missing the password_confirm field."""
        response = self.client.post(reverse("registeruser"), self.user_data_missing_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_password(self):
        """Tests the failure of creating a user due to non-matching passwords."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_email(self):
        """Tests the failure of creating a user due to an invalid email address."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_username(self):
        """Tests the failure of creating a user due to an invalid username."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_from_db(self):
        """Tests the retrieval of the first user from the database."""
        saved_user = User.objects.get(username="testuser")
        self.assertEqual(saved_user.username, "testuser")
        self.assertEqual(saved_user.email, "testuser@example.com")



    # def test_user_login(self):
    #     # user = User.objects.create_user(**self.user_data)

    #     user_data = {"username": self.user_data["username"], "password": self.user_data["password"]}
    #     login_success = self.client.login(user_data)
    #     self.assertTrue(login_success)

    #     # Optional
    #     response = self.client.get(reverse(""))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_user_get_profile(self):
    #     """Test method for getting user information"""
    #     response = self.client.get(reverse("getuser", kwargs={"user_id": 1}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data["username"], self.user_data["username"])
    #     self.assertEqual(response.data["email"], self.user_data["email"])
