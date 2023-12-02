"""Test module for views for 'oauth' app using Django REST framework"""
from rest_framework import status
from rest_framework.test import APITestCase
from useraccounts.models import User
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from oauth.views import GithubOauthAPI
import json

class GithubOauthAPITEST(APITestCase):

    def setUp(self):
        """Set up the test method for receiving a request. """
        self.factory = APIRequestFactory()
        self.url = reverse('callbackgithub')

    def test_successful_request_data(self):
         request = self.factory.post(self.url , data=json.dumps({'code': '2f9693098654ea46bc97'}).encode('utf-8'), content_type='application/json')
         ##self.assertEqual(code, "2f9693098654ea46bc97") 
         response = GithubOauthAPI.as_view()(request)
         print("response run")

    def test_missing_request_data(self):
        request = self.factory.post(self.url , data=json.dumps({}).encode('utf-8'), content_type='application/json')
        response = GithubOauthAPI.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

