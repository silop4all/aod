# -*- coding: utf-8 -*-

import sys
import httplib
import urllib
import json
from traceback import print_exc
from base64 import b64decode, b64encode
from django.conf import settings
from django.shortcuts import redirect

from config import __iam__, __openam__


class OpenamAuth(object):
    """Description of class"""

    def __init__(self):
        """ Class constructor """
        self.setAuthorizeURL()
        self.setSignupURL()

    def setAuthorizeURL(self):
        """ Generate the authorization url """
        try:
            endpoint = __iam__['base'] + __iam__['endpoints']['authorize']
            params = "?response_type=code"
            params += "&client_id=" + str(settings.CLIENT_ID)
            params += "&redirect_uri=" + urllib.quote(settings.REDIRECT_URL, safe='')
            self.authorizeURL = endpoint + params
        except:
            pass

    def getAuthorizeURL(self):
        return self.authorizeURL

    def setSignupURL(self):
        try:
            self.signupURL = __iam__['base'] + __iam__['endpoints']['signup']
        except:
            pass

    def getSignupURL(self):
        return self.signupURL

    def retrieveAccessToken(self, code, redirectUri):
        """
        Application retrieves the access token for a user from the OpenAM authorization server
        """

        try:
            endpoint = __openam__['endpoints']['access_token']
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
                "Authorization": "Basic " + b64encode(settings.CLIENT_ID + ":" + settings.CLIENT_SECRET)
            }

            payload = "grant_type=authorization_code"
            payload += "&code=" + str(code)
            payload += "&redirect_uri=" + str(redirectUri)
            connection = httplib.HTTPConnection(settings.OAUTH_SERVER)
            connection.request("POST", endpoint, payload, headers)
            response = connection.getresponse()
            return response.status, response.read()

        except Exception, e:
            print_exc()
            return 500, str(e)

    def validateAccessToken(self, accessToken):
        try:
            endpoint = __openam__['endpoints']['check_access_token']
            endpoint += "?access_token=" + str(accessToken)

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            connection = httplib.HTTPConnection(settings.OAUTH_SERVER)
            connection.request("GET", endpoint, None, headers)
            response = connection.getresponse()
            return response.status, response.read()
        except Exception, e:
            print_exc()
            return 500, str(e)

    def refreshExpiredAccessToken(self, refreshToken):
        try:
            endpoint = __openam__['endpoints']['access_token']

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + b64encode(settings.CLIENT_ID + ":" + settings.CLIENT_SECRET)
            }

            payload = "grant_type=refresh_token"
            payload += "&refresh_token=" + str(refreshToken)
            connection = httplib.HTTPConnection(settings.OAUTH_SERVER)
            connection.request("POST", endpoint, payload, headers)
            response = connection.getresponse()
            return response.status, response.read()

        except Exception, e:
            print_exc()
            return 500, str(e)

    def retrieveBasicProfile(self, accessToken):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + accessToken
            }

            connection = httplib.HTTPConnection(settings.OAUTH_SERVER)
            connection.request("GET", __openam__['endpoints']['basic_profile'], None, headers)
            response = connection.getresponse()
            return response.status, response.read()

        except Exception, e:
            print_exc()
            return 500, str(e)

    def retrieveFullyProfile(self, accessToken):
        try:
            endpoint = __iam__['endpoints']['full_profile']
            params = '?access_token=' + accessToken

            headers = {
                "Content-Type": "application/json",
            }

            connection = httplib.HTTPConnection(settings.OAUTH_SERVER)
            connection.request("GET", endpoint + params, None, headers)
            response = connection.getresponse()
            return response.status, response.read()

        except Exception, e:
            print_exc()
            return 500, str(e)

    def retrieveRolesList(self, accessToken):
        try:
            endpoint = __iam__['endpoints']['roles']

            params = '?access_token=' + accessToken + "&client_id=" + settings.CLIENT_ID

            headers = {
                "Content-Type": "application/json",
            }

            connection = httplib.HTTPConnection(settings.OAUTH_SERVER)
            connection.request("GET", endpoint + params , None, headers)
            response = connection.getresponse()
            return response.status, response.read()

        except Exception, e:
            print_exc()
            return 500, str(e)