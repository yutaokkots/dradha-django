"""Test module for views for 'oauth' app using Django REST framework"""
import json
import urllib
import re
from django.core.cache import cache
from django.urls import reverse
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
        An instance of the GithubOauthAPI class
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
        with self.subTest("Tests encoding the github code to url params - tests GithubOauthAPI.params_encoder()."):
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


            # print(parsed.find("client_id"))
            # self.assertTrue()
    
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

