"""Test module for 'useraccounts' services: useraccounts.tests.test_services"""
import django
django.setup()
from django.test import TestCase
from useraccounts.services import find_in_db, modify_username
from useraccounts.models import User

USER_DATA_SET = [
    {"username": "testuser","email": "testuser@example.com","password": "testpassword"},
    {"username": "newperson123","email": "testuser2@example.com","password": "testpassword"},
    {"username": "realuserabc","email": "testuser3@example.com","password": "testpassword"}
]

class TestUserServices(TestCase):
    """TestUserServices Class for testing User service functions (from useraccounts.tests.test_services)."""

    @classmethod
    def setUpClass(cls):
        """Method called before any tests are run."""
        super().setUpClass()
        print("\n" + cls.__doc__)

    def setUp(self):
        """Method for setting up test case."""
        self.user_data_set = USER_DATA_SET
        self.user_lst = []
        for user in self.user_data_set:
            self.user_lst.append(User.objects.create_user(**user))
        print(self.user_lst)

    def test_user_find_in_db(self):
        """Test the 'find_in_db()' function in oauth.services."""
        self.assertEqual(find_in_db("testuser"), True)
        self.assertEqual(find_in_db("inv"), False)

    def test_modify_username(self):
        """Test the 'test_modify_username()' function in oauth.services."""
        mock_user = {
            "username": "creator",
            "email": "non-unique_email@example.com",
            "password": "anypassword",
        }
        test_name = ["creator1", "13chrusername", "longercreatornamehas25chr",
                     "longercreatornamehas26chrs", "thisusernamehas27characters",
                     "anevenlongerusernamehas28chr", "approaching29characterlengths",
                     "reachingthemaxcharactername301"]

        for nm in test_name:
            print(len(nm))
        #modify_username()

    def test_usercreation(self):

        pass
        


