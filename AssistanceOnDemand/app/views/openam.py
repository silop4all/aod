# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.http import (
    Http404, 
    HttpRequest, 
    HttpResponseServerError, 
    JsonResponse, 
    HttpResponse, 
    HttpResponseRedirect
)
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import View
from rest_framework import viewsets, status

from app.models import Users, ItExperience, Providers, Consumers, Carers, Tokens
from app.views.payment import retrieve_paypal_access_token
from app.utilities import *
from app.openam import openam
from app.social_network import socialnetwork

from traceback import print_exc
from datetime import datetime
import pytz
import json
import logging
logger = logging.getLogger(__name__)


class Oauth2Login(View):
    """
    Integrate the AoD platform with the IAM/OPENAM services with respect to the login process.

    - Case 1:
    If user has been landed in the visitor area after log off, then user is directed to the IAM login form to enter the credentials and obtain access in the AoD protected area
    - Case 2:
    If the user's access_token is still valid, user is directed in the home page of the protected area
    - Case 3:
    If the user's access_token has expired but the user's refresh_token is still valid, then user's access_token, refresh_token, profile and roles has been updated and is directed in the home page of the protected area
    - Case 4:
    If both the user's access_token and refresh_token have expired, user is directed to the IAM login form to enter the credentials and obtain access in the AoD protected area
    """

    def get(self, request):
        try:
            ows = openam.OpenamAuth()
            url = ows.getAuthorizeURL()

            # if user has logged off
            if 'id' not in request.session.keys() and 'username' not in request.session.keys():
                return HttpResponseRedirect(url)

            username = request.session['username']
            tokenInstance = Tokens.objects.get(user_id=request.session['id'])
            if not tokenInstance:
                logger.info('Access token is required')
                return redirect(reverse('logout'), permanent=True)
            else:
                accessToken = tokenInstance.access_token
                refreshToken = tokenInstance.refresh_token
                status, response = ows.validateAccessToken(accessToken)

                if int(status) in [200]:
                    # Generate paypal token if user->provider and e-shop has been registered
                    retrieve_paypal_access_token(request.session['id'])
                    return redirect(reverse('home_page'), permanent=True)
                else:
                    refreshTokenStatus, refreshTokenData = ows.refreshExpiredAccessToken(refreshToken)
                    logger.info('Try to refresh the access token')
                    refreshTokenJsonData = json.loads(refreshTokenData)
                    accessToken = refreshTokenJsonData['access_token']

                    if int(refreshTokenStatus) in [200]:
                        # Retrieve the fully profile
                        fullProfileStatus, fullProfileData = ows.retrieveFullyProfile(accessToken)
                        fullProfileJson = json.loads(fullProfileData)

                        # Retrieve the list of roles
                        roles = []
                        rolesListStatus, rolesListData = ows.retrieveRolesList(accessToken)
                        rolesJson =  json.loads(rolesListData)
                        if int(rolesListStatus) == 200:
                            for i in rolesJson:
                                roles.append(i['application_role']['role'].values()[0])

                        # Update all
                        user = updateUserProfile(username, fullProfileJson)
                        updateUserRoles(user.id, roles)
                        updateUserAccessToken(user.id, refreshTokenJsonData)
                        request.session.flush()
                        setSessionValues(request, user.id, username)

                        # generate paypal token if user->provider and e-shop has been registered
                        retrieve_paypal_access_token(request.session['id'])
                        
                        return redirect(reverse('home_page'), permanent=True)

            return HttpResponseRedirect(url)
        except Exception as ex:
            logger.exception(str(ex))
            if settings.DEBUG:
                print_exc()
            return redirect(reverse('home_page'))

class Oauth2SignUp(View):

    def get(self, request):
        """Redirect user for authentication"""
        try:
            ows = openam.OpenamAuth()
            return HttpResponseRedirect(ows.getSignupURL())

        except Exception as ex:
            logger.exception(str(ex))
            raise Http404

class Callback(viewsets.ViewSet):
    """
        Retrieve the code that OpenAM authorization server provides and asks for:
            1. access token
            2. user basic profile
            3. user full profile
            4. user roles
    """

    def retrieve(self, request, *args, **kwargs):
        try:
            payload=request.GET
            redirectUri = settings.REDIRECT_URL
            code = request.GET.get('code')

            ows = openam.OpenamAuth()
            accessTokenStatus, accessTokenData = ows.retrieveAccessToken(code, redirectUri)

            if int(accessTokenStatus) == 200:
                accessTokenJsonData = json.loads(accessTokenData)
                accessToken = str(accessTokenJsonData['access_token'])
                refreshToken = str(accessTokenJsonData['refresh_token'])

                # Retrieve the basic profile
                basicProfileStatus, basicProfileData = ows.retrieveBasicProfile(accessToken)
                basicProfileJsonData= json.loads(basicProfileData)
                username = basicProfileJsonData['sub']

                # Retrieve the fully profile
                fullProfileStatus, fullProfileData = ows.retrieveFullyProfile(accessToken)
                fullProfileJson = json.loads(fullProfileData)

                # Retrieve the list of roles
                roles = []
                rolesListStatus, rolesListData = ows.retrieveRolesList(accessToken)
                rolesJson =  json.loads(rolesListData)
                if int(rolesListStatus) == 200:
                    for i in rolesJson:
                        roles.append(i['application_role']['role'].values()[0])

                userExistence = Users.objects.filter(username__exact=username).count()
                # INSERTS
                if userExistence == 0: 
                    user = insertUserProfile(fullProfileJson)
                    insertUserRoles(user.id, roles, fullProfileJson)
                    insertUserAccessToken(user.id, accessTokenJsonData)
                # UPDATES
                elif userExistence == 1:
                    user = updateUserProfile(username, fullProfileJson)
                    updateUserRoles(user.id, roles, fullProfileJson)

                    # check if token exists. If not, insert it. Otherwise, update it.
                    if Tokens.objects.filter(user_id=user.id).exists():
                        updateUserAccessToken(user.id, accessTokenJsonData)
                    else:
                        insertUserAccessToken(user.id, accessTokenJsonData)

                # check if integration with Social Network
                if socialNetworkIntegration():
                    sn = socialnetwork.SocialNetwork()
                    state, response = sn.createUser(fullProfileJson["mail"], accessToken)

                request.session.flush()
                setSessionValues(request, user.id, username)

                response = redirect(reverse('home_page'), permanent=True)
                return response
            else: 
                logger.info('No valid access token')
                return redirect(reverse('home_page'), permanent=True)

        except Exception as e:
            logger.critical(str(e))
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

def insertUserProfile(payload):
    try:
        user = Users(
            name=payload['name'], 
            lastname=payload['surname'],
            username=payload['username'], 
            gender=payload['gender'],
            pwd=-1, 
            email=payload['mail'],
            mobile=payload['phone'], 
            country=payload['country'], 
            city=payload['city'], 
            address=payload['address'], 
            postal_code=payload['postcode'], 
            is_active=True,
            experience=ItExperience.objects.get(level__iexact=payload['skills']), 
            last_login=datetime.today(),
            registration=datetime.today()
        )
        user.save()
        return user
    except Exception as ex:
        logger.exception(str(ex))
        if settings.DEBUG:
            print_exc()
        return -1

def updateUserProfile(username, payload):
    try:
        Users.objects.filter(username__exact=username).update(
            name=payload["name"], 
            lastname=payload["surname"],
            gender=payload['gender'], 
            email=payload['mail'],
            mobile=payload['phone'],
            country=payload["country"], 
            city=payload["city"], 
            address=payload["address"], 
            postal_code=payload["postcode"],
            experience=ItExperience.objects.get(level__iexact=payload['skills']),
            last_login=datetime.today()
        )
        return Users.objects.get(username__exact=username)
    except Exception as ex:
        logger.exception(str(ex))
        if settings.DEBUG:
            print_exc()
        return -1

def insertUserRoles(user_id, roles, profile):
    try:
        rolesList = ["service_provider", "service_consumer", "carer"]
        for i in rolesList:
            if i in roles:
                # cases
                if i in ["service_provider"]:
                    provider = Providers(user=Users.objects.get(pk=user_id), is_active=True, company="Not set")
                    provider.save()
                if i in ["service_consumer"]:
                    consumer = Consumers(user=Users.objects.get(pk=user_id), crowd_fund_notification=profile['crowd_fund_notification'], crowd_fund_participation=profile['crowd_fund_participation'], is_active=True)
                    consumer.save()
                if i in ["carer"]:
                    carer = Carers(user=Users.objects.get(pk=user_id), is_active=True)
                    carer.save()
            else:
                # cases
                if i in  ["service_provider"]:
                    provider = Providers(user=Users.objects.get(pk=user_id), is_active=False, company="Not set")
                    provider.save()
                if i in ["service_consumer"]:
                    consumer = Consumers(user=Users.objects.get(pk=user_id), crowd_fund_notification=profile['crowd_fund_notification'], crowd_fund_participation=profile['crowd_fund_participation'], is_active=False)
                    consumer.save()
                if i in ["carer"]:
                    carer = Carers(user=Users.objects.get(pk=user_id), is_active=False)
                    carer.save()

    except Exception as ex:
        logger.exception(str(ex))
        if settings.DEBUG:
            print_exc()
        pass

def updateUserRoles(user_id, roles, profile):
    try:
        rolesList = ["service_provider", "service_consumer", "carer"]
        if type(roles) is list:
            for i in rolesList:
                if i in roles:
                    if i in ["service_provider"]:
                        provider = Providers.objects.filter(user_id=user_id).update(is_active=True, company="Not set")
                    if i in ["service_consumer"]:
                        consumer = Consumers.objects.filter(user_id=user_id).update(crowd_fund_notification=profile['crowd_fund_notification'], crowd_fund_participation=profile['crowd_fund_participation'], is_active=True)
                    if i in ["carer"]:
                        carer = Carers.objects.filter(user_id=user_id).update(is_active=True)
                else:
                    if i in ["service_provider"]:
                        provider = Providers.objects.filter(user_id=user_id).update(is_active=False)
                    if i in ["service_consumer"]:
                        consumer = Consumers.objects.filter(user_id=user_id).update(is_active=False)
                    if i in ["carer"]:
                        carer = Carers.objects.filter(user_id=user_id).update(is_active=False)
    except Exception as ex:
        logger.exception(str(ex))
        if settings.DEBUG:
            print_exc()
        pass

def insertUserAccessToken(user_id, accessTokenJsonData):
    try:
        token = Tokens(
            user_id=user_id,
            access_token=accessTokenJsonData['access_token'],
            refresh_token=accessTokenJsonData['refresh_token'],
            expires_in=accessTokenJsonData['expires_in'],
            scope=accessTokenJsonData['scope'],
            token_type=accessTokenJsonData['token_type']
        )
        token.save()
    except Exception as ex:
        logger.exception(str(ex))
        if settings.DEBUG:
            print_exc()

def updateUserAccessToken(user_id, accessTokenJsonData):
    try:
        Tokens.objects.filter(user_id=user_id).update(
            access_token=accessTokenJsonData['access_token'],
            refresh_token=accessTokenJsonData['refresh_token'],
            expires_in=accessTokenJsonData['expires_in'],
            scope=accessTokenJsonData['scope'],
            token_type=accessTokenJsonData['token_type']
        )
    except Exception as ex:
        logger.exception(str(ex))
        if settings.DEBUG:
            print_exc()

def setSessionValues(request, user_id, username):
    try:
        request.session['id'] = user_id
        request.session['username'] = username
        request.session['cart'] = []
        request.session['is_provider']  = Providers.objects.get(user_id=user_id).is_active
        request.session['is_consumer']  = Consumers.objects.get(user_id=user_id).is_active
        request.session['is_carer'] = Carers.objects.get(user_id=user_id).is_active
    except Exception as ex:
        logger.exception(str(ex))
        if settings.DEBUG:
            print_exc()
        pass
