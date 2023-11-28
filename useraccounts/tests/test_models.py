"""Test module for 'useraccounts' models using Django REST framework"""
from django.test import TestCase
from useraccounts.models import User
from useraccounts.serializers import UserSerializer


class TestUserModel(TestCase):
    """Class for testing the user model"""

    def setUp(self):
        """Method for setting up test case."""
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_model_str_representation(self):
        """Class method for testing the user model __str__ method."""
        self.assertEqual(str(self.user), "testuser")

    def test_user_model_creation(self):
        """Test the creation of a user instance."""
        self.assertEqual(User.objects.count(), 1)
        saved_user = User.objects.get(username="testuser")
        self.assertEqual(saved_user.username, "testuser")
        self.assertEqual(saved_user.email, "testuser@example.com")
        self.assertTrue(saved_user.check_password("testpassword"))

    def test_user_serializer(self):
        """Test the UserSerializer with valid data"""
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "testuser@example.com")

    def test_user_serializer_validation(self):
        """Test the UserSerializer with invalid data"""
        invalid_data = {"username": "inv", "email": "invalid_email"}
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        # how to write error assertion test cases?
        with self.assertRaises(AssertionError):
            self.assertIn(invalid_data["username"], serializer.errors)
        with self.assertRaises(AssertionError):
            self.assertIn(invalid_data["email"], serializer.errors)
