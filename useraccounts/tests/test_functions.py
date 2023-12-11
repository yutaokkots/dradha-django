"""Test module for 'useraccounts' functions used in services: useraccounts.tests.test_services"""
import django
django.setup()
import re
from django.test import TestCase
from collections import defaultdict
from useraccounts.services import oauth_uid_generator,  oauth_uid_check_approved, oauth_uid_get_service, APPROVED_AUTH

class TestUserServiceFunctions(TestCase):
    """Tests for services functions without using the database for username storage."""

    def test_modify_username_function(self):
        """Test the 'modify_username()' function using a dictionary to store data."""
        dictionary = defaultdict(int)
        usernames_1 = ["bardo", "bardo", "bardo", "bardo", "bardo", "bardo", "bardo",
                       "bardo", "bardo", "bardo", "bardo", "bardo", "bardo", "bardo"]
        # 30 character dashes
        usernames_2 = ["------------------------------", "------------------------------",  
                       "------------------------------", "------------------------------",
                       "------------------------------", "------------------------------",
                       "------------------------------", "------------------------------",
                       "------------------------------", "------------------------------",
                       "------------------------------", "------------------------------"]
        # 29 character dashes
        usernames_3 = ["-----------------------------", "-----------------------------",  
                       "-----------------------------", "-----------------------------",
                       "-----------------------------", "-----------------------------",
                       "-----------------------------", "-----------------------------",
                       "-----------------------------", "-----------------------------",
                       "-----------------------------", "-----------------------------"]
        # 30 character dashes
        usernames_4 = ["------------------------------", "------------------------------",  
                       "------------------------------", "------------------------------",
                       "------------------------------", "------------------------------",
                       "------------------------------", "------------------------------",
                       "------------------------------", "------------------------------",
                       "------------------------------", "------------------------------"]
        # 31 character dashes
        usernames_5 = ["-------------------------------", "-------------------------------",  
                       "-------------------------------", "-------------------------------",
                       "-------------------------------", "-------------------------------",
                       "-------------------------------", "-------------------------------",
                       "-------------------------------", "-------------------------------",
                       "-------------------------------", "-------------------------------"]
        def find_username_in_dict(username):
            """Checks to see if username can be found in dictionary"""
            return username in dictionary.keys()
        
        def modify_username(username:str) -> str:
            """Mock function for 'modify_username()' in the useraccounts.services module."""
            sol_name = sub_name = username[:30] if len(username) > 30 else username
            length = len(sub_name)
            count = 1
            # modify here: find_username_in_db(sub_name) -> find_username_in_dict(username)
            while find_username_in_dict(sub_name):
                count_length = len(str(count))
                if length < 25:
                    sub_name = sol_name + str(count)
                else:
                    sub_name = sol_name[:length - count_length] + str(count)
                count += 1
            return sub_name
        with self.subTest("Subtest for adding identical usernames with length < 25"):
            for u in usernames_1:
                if u in dictionary.keys() or len(u) > 30:
                    u = modify_username(u)
                dictionary[u] += 1
            self.assertEqual(len(dictionary.keys()), len(usernames_1))
            for value in dictionary.values(): 
                self.assertEqual(value, 1, "(failure) All values should be 1.")
        with self.subTest("Subtest for adding identical usernames with length == 30"):
            for u in usernames_2:
                if u in dictionary.keys() or len(u) > 30:
                    u_mod = modify_username(u)
                    self.assertNotEqual(u, u_mod)
                    u = u_mod
                dictionary[u] += 1
            for value in dictionary.values(): 
                self.assertEqual(value, 1, "(failure) All values should be 1.")      
        with self.subTest("Subtest for adding identical usernames with length at 29, 30, and 31."):  
            # testing identical length==29 usernames. 
            for u in usernames_3:
                if u in dictionary.keys() or len(u) > 30:
                    u_mod = modify_username(u)
                    self.assertNotEqual(u, u_mod)
                    u = u_mod
                dictionary[u] += 1
            # testing identical length==30 usernames.
            for u in usernames_4:
                if u in dictionary.keys() or len(u) > 30:
                    u_mod = modify_username(u)
                    self.assertNotEqual(u, u_mod)
                    u = u_mod
                dictionary[u] += 1
            # testing identical length==31 usernames.
            for u in usernames_5:
                if u in dictionary.keys() or len(u) > 30:
                    u_mod = modify_username(u)
                    self.assertNotEqual(u, u_mod)
                    u = u_mod
                dictionary[u] += 1
            for value in dictionary.values(): 
                self.assertEqual(value, 1, "(failure) All values should be 1.")

    def test_oauth_uid_check_approved(self):
        """Test the 'oauth_uid_check_approved()' function.
        Constraints
        -----------
        oauth_login.length <= 20.
        oauth_login contains name of an approved 'auth' service followed by '-' and uid.
        name of approved 'auth' service is no more than 10 digits long
        oauth_login uid is at least 9 digits long
        """
        test_oauth_login = {
            "dradha-123230990": True,   
            "Dradha-123230990": True,   
            "Dradha123230990": False,   
            "Dradha-12!(*@&$&)()#_": False,   
            "jkj2powqmnsdw!(*@&$&)()#_": False,   
            "dradha-jdfhk": False, 
            "abcdef": False, 
            "Dradha-": False, 
            "dradha-": False, 
            "Dradha-lmsHEJd09": True, 
            "drad-lEsHJd09m": False,
            "github-lEsHJd09m": True,
            "Github-ld09mEsHJ": True, 
            "Github-dradha-ldjirj": False, 
            "dradha-ld09mEslkwejrlwkerHJ": False, 
            "google-jj239dhjk": False, 
            "dradha-jj-github-jkl": False, 
            "": False
            }
        for id, passfail in test_oauth_login.items():
            self.assertEqual(oauth_uid_check_approved(id), passfail)

    def test_oauth_login_function(self):
        """Test the 'oauth_uid_generator()' function in useraccounts.services."""
        test_oauth_login = {
            "Dradha": True,
            "dradha": True,
            "Github": True,
            "github": True,
            "google": False,
            "abcdefghijklm": False,
            "git": False,
            "goog": False,
            "": False,
            "dradhaa":False,
            "dradhaa-123456789":False,
        }
        for service, passfail in test_oauth_login.items():
            uid = oauth_uid_generator(service)
            if passfail == False:
                self.assertTrue(uid, "None")
            elif passfail == True:
                self.assertGreaterEqual(len(uid), 10)
                self.assertTrue(oauth_uid_check_approved(uid), True)

    def test_oauth_login_validation(self):
        """Test the 'modify_username()' function using a dictionary to store data"""
        dictionary2 = defaultdict(int)
        test_oauth_login = ["Dradha", "dradha", "abcdef", "Dradha", "Dradha-lmsHEJd09", 
                    "dradha-lEsHJd09m", "dradha-lEsHJd09m", 
                    "dradha-ld09mEsHJ", "dradha-ld09mEslkwejrlwkerHJ", 
                    "dradha-llwkerjHJ"]
        for ol in test_oauth_login:
            if ol in dictionary2.keys() or len(ol) > 20:
                match = re.search(r'^(.*?)-', ol)
                service = match.group(1)
                print(service)
                ol = oauth_uid_generator()
            dictionary2[ol] += 1

        print(dictionary2)

    def test_oauth_uid_get_service(self):
        test_oauth_login = {
            "dradha-123230990": True,   
            "Dradha-123230990": True,   
            "Dradha123230990": False,   
            "Dradha-12!(*@&$&)()#_": False,   
            "jkj2powqmnsdw!(*@&$&)()#_": False,   
            "dradha-jdfhk": False, 
            "abcdef": False, 
            "Dradha-": False, 
            "dradha-": False, 
            "Dradha-lmsHEJd09": True, 
            "drad-lEsHJd09m": False,
            "github-lEsHJd09m": True,
            "Github-ld09mEsHJ": True, 
            "Github-dradha-ldjirj": False, 
            "dradha-ld09mEslkwejrlwkerHJ": False, 
            "google-jj239dhjk": False, 
            "dradha-jj-github-jkl": False, 
            "": False
            }
        for test, passfail in test_oauth_login.items():
            service = oauth_uid_get_service(test)
            if not passfail:
                self.assertEqual(service, "")
            else:
                self.assertIn(service, APPROVED_AUTH)
