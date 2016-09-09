from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.conf import settings

from datetime import datetime

from app.models import Users, Tokens, Providers, Consumers, Carers, ItExperience
from app.openamAuth import *

def loginRequired(function):
    """
    Check if the user is connected
    Decorator for function-based  views 
    """
    def wrap(request, *args, **kwargs):
        # If logout
        if 'id' not in request.session.keys() and 'username' not in request.session.keys():
            request.session.flush()
            return redirect(reverse('login_page'), permanent=True)

        ows             = OpenamAuth()
        url             = ows.getAuthorizeURL()
        username        = request.session['username']
        tokenInstance   = Tokens.objects.get(user_id=request.session['id'])

        if not tokenInstance:
            if settings.DEBUG:
                print 'Access token is required'
            # redirect initially to AOD inform page - 401
            request.session.flush()
            return redirect(reverse('login_page'), permanent=True)

        accessToken     = tokenInstance.access_token
        refreshToken    = tokenInstance.refresh_token
        accessTokenStatus, response= ows.validateAccessToken(accessToken)

        # if access_token has expired
        if int(accessTokenStatus) not in [200]:
            refreshTokenStatus, refreshTokenData = ows.refreshExpiredAccessToken(refreshToken)

            # if refresh_token is still valid
            if int(refreshTokenStatus) in [200]:  
                refreshTokenJsonData= json.loads(refreshTokenData)
                accessToken         = refreshTokenJsonData['access_token']
                
                # Retrieve the fully profile
                fullProfileStatus, fullProfileData = ows.retrieveFullyProfile(accessToken)
                fullProfileJson     = json.loads(fullProfileData)

                # Retrieve the list of roles
                roles = []
                rolesListStatus, rolesListData = ows.retrieveRolesList(accessToken)
                rolesJson =  json.loads(rolesListData)
                if int(rolesListStatus) == 200:
                    for i in rolesJson:
                        roles.append(i['application_role']['role'].values()[0])

                # Update all
                Users.objects.filter(username__exact=username).update(
                    name=fullProfileJson["name"], 
                    lastname=fullProfileJson["surname"],
                    gender=fullProfileJson['gender'], 
                    email=fullProfileJson['mail'],
                    mobile=fullProfileJson['phone'],
                    country=fullProfileJson["country"], 
                    city=fullProfileJson["city"], 
                    address=fullProfileJson["address"], 
                    postal_code=fullProfileJson["postcode"],
                    experience=ItExperience.objects.get(level__iexact=fullProfileJson['skills']),
                    last_login=datetime.today()
                )
                user =  Users.objects.get(username__exact=username)

                rolesList = ["service_provider", "service_consumer", "carer"]
                if type(roles) is list:
                    for i in rolesList:
                        if i in roles:
                            if i in ["service_provider"]:
                                provider = Providers.objects.filter(user_id=user.id).update(is_active=True, company="Not set")
                            if i in ["service_consumer"]:
                                consumer = Consumers.objects.filter(user_id=user.id).update(crowd_fund_notification=False, crowd_fund_participation=False, is_active=True)
                            if i in ["carer"]:
                                carer = Carers.objects.filter(user_id=user.id).update(is_active=True)
                        else:
                            if i in ["service_provider"]:
                                provider = Providers.objects.filter(user_id=user.id).update(is_active=False)
                            if i in ["service_consumer"]:
                                consumer = Consumers.objects.filter(user_id=use.id).update(is_active=False)
                            if i in ["carer"]:
                                carer = Carers.objects.filter(user_id=user.id).update(is_active=False)

                Tokens.objects.filter(user_id=user.id).update(
                    access_token=refreshTokenJsonData['access_token'],
                    refresh_token=refreshTokenJsonData['refresh_token'],
                    expires_in=refreshTokenJsonData['expires_in'],
                    scope=refreshTokenJsonData['scope'],
                    token_type=refreshTokenJsonData['token_type']
                )

                request.session.flush()
                request.session['id'] = user.id
                request.session['username'] = username
                request.session['cart'] = []
                request.session['is_provider']  = Providers.objects.get(user_id=user.id).is_active
                request.session['is_consumer']  = Consumers.objects.get(user_id=user.id).is_active
                request.session['is_carer']     = Carers.objects.get(user_id=user.id).is_active
            else:
                # redirect initially to AOD inform page - 401
                request.session.flush()
                return redirect(reverse('login_page'), permanent=True)


        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def loginRequiredView(View): 
    """
    Check if the user is connected
    Decorator for class-based views 
    """
    View.dispatch = method_decorator(loginRequired)(View.dispatch)
    return View