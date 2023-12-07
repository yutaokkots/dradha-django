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
            auth_token = self.githuboauthapi.parse_access_token(self.response_tokenesponse)
            self.assertEqual(auth_token, "abcdefaccess1234token56789")

        with self.subTest("Test parsing values for User model from the HTTP response(from Github)."):
            """Tests GithubOauthAPI.parse_for_user_model()"""


        with self.subTest("Test parsing values for Profile model from the HTTP response(from Github)."):
            """Tests GithubOauthAPI.parse_for_profile_model()"""


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

