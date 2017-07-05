# -*- coding: utf-8 -*-

import httplib
import urllib
from traceback import print_exc
from django.conf import settings

import logging
logger = logging.getLogger(__name__)


class SocialNetwork(object):
    """Class for social network component"""


    def __init__(self):
        """ Class constructor """
        pass


    def createUser(self, email, accessToken):
        """
        Create a user in Social Network (if new in AoD)
        """

        try:
            endpoint = settings.SOCIAL_NETWORK_WEB_SERVICES['users']['insert']
            endpoint += "/email/" + str(email) 
            endpoint += "/access-token/" + str(accessToken)
            
            headers = {
                "Authorization": "Basic " + settings.SOCIAL_NETWORK_WEB_SERVICES_AUTH
            }

            connection = httplib.HTTPConnection(settings.SOCIAL_NETWORK_WEB_SERVICES['url'])
            connection.request("POST", endpoint, None, headers)
            response = connection.getresponse()
            return response.status, response.read()

        except Exception, e:
            logger.critical(str(e))
            print_exc()
            return 500, str(e)


    def sessionLogout(self, userId):
        """
        Logout a specific user from the Social Network
        """
        try:
            endpoint = settings.SOCIAL_NETWORK_WEB_SERVICES['sessions']['logout']
            endpoint += str(userId) 

            headers = {
                "Authorization": "Basic " + settings.SOCIAL_NETWORK_WEB_SERVICES_AUTH
            }

            connection = httplib.HTTPConnection(settings.SOCIAL_NETWORK_WEB_SERVICES['url'])
            connection.request("GET", endpoint, None, headers)
            response = connection.getresponse()
            return response.status, response.read()

        except Exception, e:
            logger.critical(str(e))
            print_exc()
            return 500, str(e)