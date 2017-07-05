# -*- coding: utf-8 -*-

import sys
import httplib
import urllib
import requests
import json
from traceback import print_exc
from django.conf import settings

from config import __payment__


class P4ABase(object):
    """ P4A Payment class
    """


    client_id = settings.CLIENT_ID


    def __init__(self, access_token, paypal_token):
        """Class constructor

        :param access_token: the access_token of user (OpenAM)
        :type access_token: string
        :param paypal_token: the paypal_token of provider (Paypal)
        :type paypal_token: string
        """
        self.__payment__ = __payment__
        #self.__paypal__ = __paypal__
        
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Openam-Client": str(Payment.client_id),
            "Openam-Client-Token": str(access_token),
            "Paypal-Access-Token": str(paypal_token)
        }

class BillingPlan(P4ABase):
    """Manage billing plan actions 
    """

    def create(self, payload):
        """Create a billing plan via P4A component

        Usage::
            >>> from app.payment import p4a_payment as payment
            >>> plan = payment.BillingPlan(__access_token__, __paypal_token__)
            >>> (http_status, response_json) = plan.create(__dict__)

        :param payload: the billing plan details (paypal data format)
        :type payload: dictionary
        :returns: the HTTP status and the response body
        :rtype: tuple(integer, dictionary)
        """
        try:
            endpoint = str(self.__payment__['base']['api']) + str(self.__payment__['endpoints']['billing_plans'])
            request = requests.post(endpoint, data=json.dumps(payload), headers=self.headers, verify=False)
            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except:
            return 500, dict({"error": "Internal server error"})


    def activate(self, plan_id):
        """Activate a billing plan via P4A component

        Usage::
            >>> from app.payment import p4a_payment as payment
            >>> plan = payment.BillingPlan(__access_token__, __paypal_token__)
            >>> (http_status, response_json) = plan.activate(plan_id)

        :param plan_id: the billing plan id as provided from the Paypal, i.e. P-xxxxxxxxx 
        :type plan_id: string
        :returns: the HTTP status and the response body
        :rtype: tuple(integer, dictionary)
        """
        try:
            endpoint = str(self.__payment__['base']['api']) + str(self.__payment__['endpoints']['billing_plans']) 
            endpoint += "/" + str(plan_id)
            request = requests.patch(endpoint, data=None, headers=self.headers, verify=False)
            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except:
            return 500, dict({"error": "Internal server error"})

class BillingAgreement(P4ABase):
    """Manage billing agreement actions"""

    def create(self, payload):
        """Create a billing agreement via P4A component

        Usage::
            >>> from app.payment import p4a_payment as payment
            >>> agreement = payment.BillingAgreement(__access_token__, __paypal_token__)
            >>> (http_status, response_json) = agreement.create(__dict__)

        :param payload: the description of billing agreement 
        :type payload: dictionary/JSON
        :returns: the HTTP status and the response body (if any)
        :rtype: tuple(integer, dictionary)
        """
        try:
            endpoint = str(self.__payment__['base']['api']) + str(self.__payment__['endpoints']['billing_agreements'])
            request = requests.post(endpoint, json=json.dumps(payload), headers=self.headers, verify=False)
            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except Exception as ex:
            return 500, dict({"error":"Internal server error"})

    def execute(self, payment_token):
        """Execute a billing agreement after customer confirmation

        Usage::
            >>> from app.payment import p4a_payment as payment
            >>> agreement = payment.BillingAgreement(__access_token__, __paypal_token__)
            >>> (http_status, response_json) = agreement.execute(__string__)

        :param payment_token: the payment_token provided from the paypal, i.e. EC-xxxxxxxxxxx
        :type payment_token: string
        :returns: the HTTP status and the response body (if any)
        :rtype: tuple(integer, dictionary)
        """
        try:
            endpoint = str(self.__payment__['base']['api']) + str(self.__payment__['endpoints']['billing_agreements'])
            endpoint += "/" + str(payment_token) + "/" + "agreement-execute"
            request = requests.post(endpoint, data=None, headers=self.headers, verify=False)
            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except:
            return 500, dict({"error":"Internal server error"})


class Payment(P4ABase):

    def create(self, payload):
        """Send a payment  request to P4A Payment mechanism

        :param payload: the description of payment 
        :type payload: dictionary
        :returns: the HTTP status and the response body (if any)
        :rtype: tuple(integer, dictionary)
        """
        try:
            endpoint = str(self.__payment__['base']['api']) + str(self.__payment__['endpoints']['payments'])
            request = requests.post(endpoint, data=json.dumps(payload), headers=self.headers, verify=False)
            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except:
            print_exc()
            return 500, dict({"error": "Internal server error"})

    def execute(self, pay_id, payer_id):
        """Execute the payment transaction after consumer approval

        :param pay_id: the payment token, eg EC-xxxxxxx
        :type pay_id: string
        :returns: the HTTP status and the response body (if any)
        :rtype: tuple(integer, dictionary)
        """        
        try:
            endpoint = str(self.__payment__['base']['api']) + str(self.__payment__['endpoints']['payments']) 
            endpoint += "/" + str(pay_id) + "/execute"

            payload = {"payer_id": str(payer_id)}
            request = requests.post(endpoint, data=json.dumps(payload), headers=self.headers, verify=False)

            try:
                return request.status_code, request.json()
            except ValueError as ex:
                return request.status_code, dict({"error": request.reason})
        except:
            print_exc()
            return 500, dict({"error": "Internal server error"})    