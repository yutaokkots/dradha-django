from django.shortcuts import render
from rest_framework import status, request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import redirect
from django.core.cache import cache
from django.http import HttpResponseServerError
import requests
import logging
import os
from urllib.parse import urlsplit, parse_qs
import urllib.parse
import random
import string
import json
from datetime import datetime

# test that I receive something at the callback route
# code
# state (user provided)

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
            # cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None) # DEFAULT_TIMEOUT is in seconds, an int. 
            print(response)
            return Response(data=response, status=status.HTTP_201_CREATED)
        except ValueError as value_error:
            error_message = f"ValueError: {value_error}"
            return Response(data={"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def state_generator(self, length:int) -> str:
        code = [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
        return "".join(code)
    
    def timestamp(self):
        return json.dumps(datetime.now().isoformat())
    
    def set_state(self, state):
        """Saves the generated state in cache with a time-out of 10 minutes (600 seconds)."""
        key_state = state[:5]
        cache.set(key_state, state, timeout=600) 

class GithubOauthAPI(APIView):
    """ Class for the callback route once user submits login information 
    for Github OAuth2 authenticaion. 
    """
    
    def get(self, request, *args, **kwargs):
        try: 
            params = request.query_params
            params_state = params["state"]
            code = params["code"]
            if self.verify_state(params_state) and code:
                url = GITHUB_URL
                params = self.params_parser(code)
                response = requests.post(url=url, params=params)

                response_data = str(response.content, encoding='utf-8')
                # response_data = 'access_token=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&scope=&token_type=bearer'
                # print(response_data)
  
                parameters = parse_qs(response_data)
                # print(parameters)
                # print(parameters["access_token"])
                # print(parameters["access_token"][0])
                
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
        """ Gets the state by its key (first 5 chars), and verifies the cached state is equal to the input state."""
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
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.get(GITHUB_URL_USER, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error accessing token: {e}")
            return None





    def post(self, request, *args, **kwargs):
        print("POST!")
        # try:
        #     self.code = request.data["code"]
        # except KeyError as e:
        #     return Response({"error": f"Missing {e} parameter"}, status=status.HTTP_400_BAD_REQUEST)
        # urlparams = self.post_github()
        # #
        # self.access_token_url = f"{GITHUB_URL}?{urlparams}"
        # print(self.access_token_url)
        # #logging.info(self.access_token_url)
        # print(self.token_access())
        # return Response({}, status=status.HTTP_201_CREATED)
    


