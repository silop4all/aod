# -*- coding: utf-8 -*-

import sys
import httplib
import urllib
from traceback import print_exc
from django.conf import settings
import requests

from config import __base_map__, __endpoint_map__


class Microlabora(object):
    """Class that handles the interaction with Microlabora web services
    """

    def __init__(self, access_token):
        """Class constructor

        Usage::
            >>> from app.microlabora import microlabora as ml

        :param access_token: the authentication token generated from the OpenAM 
        :type access_token: string
        """

        self.__base_map__ = __base_map__
        self.__endpoint_map__ = __endpoint_map__
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authentication": "Bearer " + str(access_token)
        }


class Task(Microlabora):
    """Task class that inherits the Microlabora class
    """
    
    def publish(self, payload):
        """Publish a new human task in Microlabora

        Usage::
            >>> from app.microlabora import microlabora as ml
            >>> task = ml.Task("access_token")
            >>> (http_status, response_json) = task.publish("task_as_json")

        :param payload: the description of task 
        :type payload: JSON
        :returns: the HTTP status and the response body (if any)
        :rtype: tuple(integer, dictionary)
        """

        try:
            endpoint = str(self.__base_map__['api']) + str(self.__endpoint_map__['publish_service'])
            request = requests.post(endpoint, json=payload, headers=self.headers)

            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except Exception as e:
            return 500, dict({"error": str(e)})