"""Class-based views for the oauth and oauth related uri endpoints."""
import urllib
import logging
import random
import json
from datetime import datetime
import os
import string
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from django.core.cache import cache
from django.http import HttpResponseServerError

GITHUB_URL = 'https://github.com/login/oauth/access_token' # os.environ['SECRET_GITHUB_TOKEN_URL'] #
GITHUB_URL_USER = 'https://api.github.com/user'

class GithubStateGenerator(APIView):
    """Class for generating and storing a state for Github OAuth Authorization"""

    def get(self, request, *args, **kwargs):
        """Method for returning a randomly generated state for OAuth Authentication"""
        try:
            length = 20
            rand_state = self.state_generator(length)
            ts = self.timestamp()
            response = {
                "state":rand_state,
                "timestamp":ts,
            }
            self.set_state(rand_state)

            print(response)
            return Response(data=response, status=status.HTTP_201_CREATED)
        except ValueError as value_error:
            error_message = f"ValueError: {value_error}"
            return Response(data={"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def state_generator(self, length:int) -> str:
        """Generates a random state of length, 'length:int'. """
        code = [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
        return "".join(code)

    def timestamp(self) -> str:
        """Creates an ISO format timestamp"""
        return json.dumps(datetime.now().isoformat())

    def set_state(self, state):
        """Saves the generated state in cache with a time-out of 10 minutes (600 seconds).

        For caching in psql database:
        cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None) 
        # DEFAULT_TIMEOUT is in seconds, an int.
        """
        key_state = state[:5]
        cache.set(key_state, state, timeout=600)

class GithubOauthAPI(APIView):
    """ Class for the callback route once user submits login information 
    for Github OAuth2 authenticaion. 
    """

    def get(self, request, *args, **kwargs):
        """GET HTTP method for the callback URI for requesting an Auth token from Github."""
        try:
            params = request.query_params
            params_state = params["state"]
            code = params["code"]
            if self.verify_state(params_state) and code:
                url = GITHUB_URL
                params = self.params_parser(code)
                timeout_seconds = 10
                response = requests.post(url=url, params=params, timeout=timeout_seconds)
                response_data = str(response.content, encoding='utf-8')
                parameters = urllib.parse.parse_qs(response_data)

                access_token = parameters["access_token"][0]

                user = self.user_access(access_token)
                print(user)
                response.raise_for_status()
        except ValueError as ve:
            return HttpResponseServerError(f"Error: {ve}")
        except requests.RequestException as re:
            return HttpResponseServerError(f"Request Error: {re}")
        except Exception as e:
            return HttpResponseServerError(f"Unexpected Error: {e}")
        return redirect('http://localhost:3000')

    def verify_state(self, state:str):
        """ Gets the state by its key (first 5 chars), 
            and verifies the cached state is equal to the input state.
        """
        value = cache.get(state[:5])
        print(value == state)
        return value == state

    def params_parser(self, auth_code):
        """ Creates the url encoded parameters. """
        parameters = {
            "client_id": os.environ['SECRET_ID_GITHUB'], 
            "client_secret": os.environ['SECRET_KEY_GITHUB'], 
            "code": auth_code, 
            "redirect_uri": "http://localhost:8000/oauth/callback/"
        }
        return urllib.parse.urlencode(parameters)


    def user_access(self, auth_token):
        """ Accesses the user information from the Github server."""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            timeout_seconds = 10
            response = requests.get(GITHUB_URL_USER, headers=headers, timeout=timeout_seconds)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error accessing token: {e}")
            return None
