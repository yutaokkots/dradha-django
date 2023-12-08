"""Test module for views for 'oauth' app using Django REST framework"""
import json
import urllib
import re
from unittest.mock import MagicMock
from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from oauth.views import GithubOauthAPI, GithubStateGenerator
from useraccounts.models import User

    # 'login': 'ace123',
    # 'avatar_url': 'https://avatars.githubusercontent.com/u/1234567890123', 
    # 'email': None, 
    # 'oauth_login

USER_INFO = {
    'login': 'ace123',
    'id': 1234567890123, 
    'node_id': 'xxxxxx', 
    'avatar_url': 'https://avatars.githubusercontent.com/u/1234567890123', 
    'gravatar_id': '', 
    'url': 'https://api.github.com/users/ace123', 
    'html_url': 'https://github.com/ace123', 
    'followers_url': 'https://api.github.com/users/ace123/followers', 
    'following_url': 'https://api.github.com/users/ace123/following{/other_user}', 
    'gists_url': 'https://api.github.com/users/ace123/gists{/gist_id}', 
    'starred_url': 'https://api.github.com/users/ace123/starred{/owner}{/repo}', 
    'subscriptions_url': 'https://api.github.com/users/ace123/subscriptions', 
    'organizations_url': 'https://api.github.com/users/ace123/orgs', 
    'repos_url': 'https://api.github.com/users/ace123/repos', 
    'events_url': 'https://api.github.com/users/ace123/events{/privacy}', 
    'received_events_url': 'https://api.github.com/users/ace123/received_events', 
    'type': 'User', 
    'site_admin': False, 
    'name': 'FirstName LastName', 
    'company': None, 
    'blog': 'https://www.dradha.co', 
    'location': 'Somewhere, CA', 
    'email': None, 
    'hireable': None, 
    'bio': 'Full-Stack Developer', 
    'twitter_username': None, 
    'public_repos': 29, 
    'public_gists': 0, 
    'followers': 26, 
    'following': 37, 
    'created_at': '2017-11-15T00:14:48Z', 
    'updated_at': '2023-11-26T06:36:59Z'
}

USER_KEY = {
    "username":'login',
    'email':'email',
    'avatar_url':'avatar_url',
    'oauth_login':'oauth_login'
}
    
PROFILE_KEY = {
    "bio": "bio",
    "company": "company",
    "github_url":"html_url",
    "website": "blog",
    "location":"location",
    "twitter_username":"twitter_username"
}

class GithubStateAPITEST(APITestCase):
    """Class for testing the OAuth endpoint for this app. 

    Attributes
    ----------
    self.factory : metaclass
        Instance of APIRequestFactory for creating a request. 
    self.url_callback : string
        URI endpoint of "api/oauth/callback/" | GET.
    self.requestbody : dict
        A mock request body. 
    self.request : class instance
        A mock request instance. 
    self.githuboauthapi : class instance
        An instance of the GithubOauthAPI class.
    self.response_state : string
    self.response_token : HTTP object
        A mock response containing token information.
    self.user_info : dict
    """

    def setUp(self):
        """Set up the test method for receiving a request."""
        self.factory = APIRequestFactory()
        self.url_callback = reverse('callback')
        self.requestbody = {
            "client_code": "abcdef",
            "length": 20,
        }
        self.request = self.factory.get(self.url_callback) ##, content_type='application/json', data=self.requestbody)
        self.githuboauthapi = GithubOauthAPI()
        self.response_state = ""
        content = b'access_token=abcdefaccess1234token56789&scope=&token_type=bearer'
        self.response_token = HttpResponse(content=content,  status=status.HTTP_200_OK)
        self.response_token["Accept"] = "application/json"
        self.user_info = USER_INFO

    def test_success_get_state(self):
        """Test to retrieve a randomly generated state from the 'api/oauth/callback/state' URI."""
        response = GithubStateGenerator.as_view()(self.request)
        self.assertIn('state', response.data)
        self.assertIn('timestamp', response.data)
        self.assertTrue(response.data['state'])
        self.assertTrue(response.data['timestamp'])
        self.assertEqual(len(response.data['state']), self.requestbody["length"])
        self.response_state = response.data['state']

    def test_githuboauthapi_class(self):
        """Tests the methods inside the GithubOauthAPI class"""
        with self.subTest("Tests encoding the github code to url params."):
            """Tests GithubOauthAPI.params_encoder()"""
            code = "3908e6ff54e9a46bc"
            result = self.githuboauthapi.params_encoder(code)
            self.assertTrue(type(result), str)
            parsed = urllib.parse.unquote(result)
            parsed_lst = parsed.split("&")
            self.assertTrue(len(parsed_lst), 4)
            test_params = ["client_id=", "client_secret=", "code=", "redirect_uri="] 
            for element in parsed_lst:
                key_match = re.search(r"(.*?)=", element)
                key_str = key_match.group()
                value_match = re.search(r"=(.*)", element)
                value_str = value_match.group(1)
                self.assertEqual(key_str in test_params, True)
                self.assertNotEqual(value_str, "")
                if key_str == "code=":
                    self.assertEqual(value_str, code)

        with self.subTest("Tests parsing the access token from the HTTP response (from Github)."):
            """Tests GithubOauthAPI.parse_access_token()."""
            auth_token = self.githuboauthapi.parse_access_token(self.response_token)
            self.assertEqual(auth_token, "abcdefaccess1234token56789")

        with self.subTest("Test parsing values for User model from the HTTP response(from Github)."):
            """Tests GithubOauthAPI.parse_for_user_model()"""
            parsed_user = self.githuboauthapi.parse_for_user_model(self.user_info)
            for key in parsed_user.keys():
                if key == "oauth_login":
                    self.assertGreater(len(parsed_user[key]), 7)
                    continue
                self.assertEqual(parsed_user[key], self.user_info[USER_KEY[key]])

        with self.subTest("Test parsing values for Profile model from the HTTP response(from Github)."):
            """Tests GithubOauthAPI.parse_for_profile_model()"""
            parsed_profile = self.githuboauthapi.parse_for_profile_model(self.user_info)
            for key in parsed_profile.keys():
                self.assertEqual(parsed_profile[key], self.user_info[PROFILE_KEY[key]])


    # def test_success_post(self):
    #     request = self.factory.post(self.url, json.dumps(self.requestbody), content_type='application/json')
    #     response = GithubOauthAPI.as_view()(request)
    #     print(f"{response=}")
    #     print(f"{response.data=}")
    

        #self.assertContains(status_code=201, response=response, text="response")

    # def test_token_generator(self):

    #     response = GithubOauthAPI.as_view(get='get')()
    # def test_successful_request_data(self):
    #      request = self.factory.post(self.url , data=json.dumps({'code': '2f9693098654ea46bc97'}).encode('utf-8'), content_type='application/json')
    #      ##self.assertEqual(code, "2f9693098654ea46bc97") 
    #      response = GithubOauthAPI.as_view()(request)
    #      print("response run")

    # def test_missing_request_data(self):
    #     request = self.factory.post(self.url , data=json.dumps({}).encode('utf-8'), content_type='application/json')
    #     response = GithubOauthAPI.as_view()(request)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

