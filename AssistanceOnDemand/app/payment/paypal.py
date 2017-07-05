# -*- coding: utf-8 -*-

import sys
import httplib
import urllib
import json
import requests
from traceback import print_exc
from django.conf import settings
from base64 import b64encode


from config import __paypal__


class Paypal(object):
    """Paypal class
    """

    def __init__(self, client_id, client_secret):
        """Class constructor

        :param client_id: the client_id of the merchant e-shop in Paypal
        :type client_id: string
        :param client_secret: the client_secret of the merchant e-shop in Paypal
        :type client_secret: string        
        """
        self.__paypal__ = __paypal__
        self.authorization = b64encode(str(client_id) + ":" + str(client_secret))

        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json"
        }




class Token(Paypal):
    """Token class that inherits the Paypal class
    """

    def generate(self):
        """Generate the Access token in Paypal based on provider app credentials in Paypal

        Usage::
            >>> from app.payment import paypal
            >>> paypal_token = paypal.Token("client_id", "client_secret")
            >>> (http_status, response_json) = paypal_token.generate()

        :returns: the HTTP status and the response body (if any)
        :rtype: tuple(integer, dictionary)
        """
        try:
            self.headers["Authorization"] = "Basic " + str(self.authorization)
            self.headers["Content-type"] = "application/x-www-form-urlencoded"
            endpoint = str(self.__paypal__['base']['sandbox']) + str(self.__paypal__['endpoints']['authentication'])
            request = requests.post(endpoint, data="grant_type=client_credentials", headers=self.headers)
            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except:
            return 500, dict({"error":"Internal server error"})


class BillingAgreement(object):

    def __init__(self, bearer_token):
        """Class constructor"""

        self.__paypal__ = __paypal__
        self.bearer_token = bearer_token
        self.headers = {
            "Authorization": "Bearer " + str(self.bearer_token),
            "Content-Type": "application/json"
        }


    def cancel(self, agreement_id):
        """Cancel a existing billing agreement"""

        try:
            endpoint = str(self.__paypal__['base']['sandbox']) + str(self.__paypal__['endpoints']['billing_agreements'])
            endpoint += "/" + str(agreement_id) + "/" + "cancel"

            payload = {"note": "Cancel the subscription"}
            request = requests.post(endpoint, data=json.dumps(payload), headers=self.headers, verify=False)

            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except:
            return 500, dict({"error":"Internal server error"})

