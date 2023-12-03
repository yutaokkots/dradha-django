"""Test module for views for 'oauth' app using Django REST framework"""
from rest_framework import status
from rest_framework.test import APITestCase
from useraccounts.models import User
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from oauth.views import GithubOauthAPI, GithubStateGenerator
import json

class GithubStateAPITEST(APITestCase):

    def setUp(self):
        """Set up the test method for receiving a request. """
        self.factory = APIRequestFactory()
        self.url = reverse('callback')
        self.requestbody = {
            "client_code": "abcdef",
            "length": 20,
        }

    def test_success_get_state(self):
        request = self.factory.get(self.url) ##, content_type='application/json', data=self.requestbody)
        response = GithubStateGenerator.as_view()(request)
        self.assertIn('state', response.data)
        self.assertIn('timestamp', response.data)
        self.assertTrue(response.data['state'])
        self.assertTrue(response.data['timestamp'])
        self.assertEqual(len(response.data['state']), self.requestbody["length"])
    

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

