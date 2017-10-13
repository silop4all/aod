# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import (
    render, 
    redirect, 
    render_to_response, 
    get_object_or_404
)
from django.http import (
    Http404, 
    HttpRequest, 
    HttpResponseServerError, 
    JsonResponse, 
    HttpResponse, 
    HttpResponseRedirect,
    HttpResponseForbidden
)
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.views.generic import (
    View, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    ListView
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (
    require_http_methods, 
    require_GET, 
    require_POST, 
    require_safe
)
from django.core import serializers
from django.core.exceptions import (
    ObjectDoesNotExist, 
    MultipleObjectsReturned
)
from django.conf import settings
from django.contrib import messages
from django.db.models import (
    Avg, 
    Sum, 
    Q
)
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils import translation
from rest_framework import viewsets, status

from app.models import *        # import models
from app.decorators import *    # import custom models
from app.utilities import *
from app.openam import openam
from app.social_network import socialnetwork
from app.microlabora import microlabora as ml
from app.views.payment import retrieve_paypal_access_token
from app.payment import p4a_payment, paypal

from restapi.serializers import (
    UserThemeSerializer, 
    SimpleServiceSerializer,
    SimpleServiceTechnicalSupportSerializer
)


import os
from functools import wraps
from datetime import datetime, timedelta, date
import pytz
import json
from traceback import print_exc
from base64 import b64decode, b64encode
import httplib
import urllib
import hashlib

import logging
logger = logging.getLogger(__name__)



#==============================
#   Translations
#==============================
def changeLanguage(request):
    if request.method == "POST":
        try:
            language = request.POST.get('language')
            next = request.POST.get('next')

            if 'HTTP_REFERER' in request.META:
                referer = request.META['HTTP_REFERER']
            if 'HTTP_ORIGIN' in request.META:
                origin = request.META['HTTP_ORIGIN']
            else:
                origin = str(settings.AOD_HOST['PROTOCOL']) + "://" 
                origin += str(settings.AOD_HOST['IP']) + ":" + str(settings.AOD_HOST['PORT'])
                origin += str(settings.AOD_HOST['PATH'])

            if settings.DEBUG:
                print origin

            translation.activate(language)
            ll = [v[0] for i,v in enumerate(settings.LANGUAGES)]
            path = referer.replace(origin, '')
            new_path = [v if v not in ll else language for i,v in enumerate(path.split('/'))]
            next = '/'.join(new_path)

            response = redirect(next)
            expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=settings.LANGUAGE_COOKIE_AGE), "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, settings.LANGUAGE_COOKIE_AGE, expires)
            return response
        except Exception as ex:
            logger.error(str(ex))
            if settings.DEBUG:
                print_exc()
            raise HttpResponseServerError()


#==============================
#   Presentation Themes
#==============================
class PresentationThemesView(View):
    def get(self, request):
        """
        Load a list of app themes
        """
        try:
            template = 'app/preferences/themes/index.html'
            if 'id' not in request.session.keys():
                return redirect(reverse('login_page'))
            pk = request.session['id']
            themesList = Theme.objects.all()
            try:
                selectedTheme = UserTheme.objects.get(user_id=pk)
            except ObjectDoesNotExist:
                selectedTheme = None
        
            return render(request, template,
                context_instance = RequestContext(request, 
                {
                    "themesList" : themesList,
                    "selectedTheme": selectedTheme,
                    "title": _("Select your favorite theme"),
                }))
        except:
            print_exc()
            raise Http404

class PresentationTheme(View):
    def post(self, request, theme_id):
        """
        Store the theme that user prefers
        """
        try:
            user = Users.objects.get(pk=request.session['id'])
            theme =Theme.objects.get(pk=theme_id)
            payload = {"user": int(user.id),"theme": int(theme.id)}
            serializer = UserThemeSerializer(data=payload)
            response = redirect(reverse('preferences_themes'))
            
            if serializer.is_valid():
                userTheme = UserTheme.objects.filter(user=user)
                if userTheme.count():
                    userTheme.update(**payload)
                else:
                    instance = UserTheme(user_id=user.id,theme_id=theme.id)
                    instance.save()
    
                expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=settings.LANGUAGE_COOKIE_AGE), "%a, %d-%b-%Y %H:%M:%S GMT")
                response.set_cookie(settings.THEME_COOKIE_NAME, theme_id, settings.LANGUAGE_COOKIE_AGE, expires)
            else:
                print serializer.errors
            return response
        except:
            if settings.DEBUG:
                print_exc()
            raise Http404



#==============================
#   Visitor area
#==============================
class IndexView(View):
    """Manage index page
    """

    def get(self, request):
        """Load AoD index page 
        """
        try:
            assert isinstance(request, HttpRequest)

            if settings.CUSTOMIZATION_PROCESS:
                template = "app/home/customizedIndex.html"
                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'year': datetime.now().year,
                        'sortby': request.GET.get('sortby', None),
                        'technicalSupport': TechnicalSupport.objects.all().order_by('type'),
                        'help': Topic.objects.filter(visible=True).order_by('title'),
                        'services': Services.objects.filter(is_visible=True),
                        'ml_categories': TaskCategory.objects.all()
                    })
                )
            else:
                template = "app/home/index.html"
                providers, types, chargingModels = list(), list(), list()

                # Try different
                refine_search = False
                preferences = None
                if 'id' in request.session and request.GET.get('action', None) is not None:
                    refine_search = True
                    user_id = request.session['id']
                    track = TrackUserSearch.objects.filter(user_id=user_id)
                    if track.count():
                        preferences = track.first().preferences

                for i in Providers.objects.filter(is_active=True):
                    user =  Users.objects.get(id=i.user_id)
                    providers.append({"id": i.id, "name": user.name, "lastname": user.lastname, 
                        "count": Services.objects.filter(owner_id=i.id).exclude(is_visible=False).count()})

                for i in list(ALL_CHOICES):
                    types.append({ "type" : str((i[1].split(" ")[0]).lower()), "alias": str(i[0].lower()), 
                        "count": Services.objects.filter(type=i[0]).exclude(is_visible=False).count() })

                for model in ChargingPolicies.objects.all().order_by("id"):
                    chargingModels.append({"id": model.id, "name":model.name, 
                        "servNo": Services.objects.filter(charging_policy_id=model.id).exclude(is_visible=False).count() })

                # find if user participated in communities
                participate_in_communities = False
                community_cookie_existence = False if request.COOKIES.get(settings.COMMUNITY_COOKIE_NAME, False) == False else True

                if 'id' in request.session.keys():
                    user = Users.objects.get(pk=request.session['id'])
                    participate_in_communities = user.community_participation


                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'year': datetime.now().year,
                        'providers': providers,
                        'types': types,
                        'chargingModels': chargingModels,
                        'sortby': request.GET.get('sortby', None),
                        'ml_categories': TaskCategory.objects.all(),
                        'participate_in_communities': participate_in_communities,
                        'community_cookie_existence': community_cookie_existence,
                        'refine_search': refine_search,
                        'preferences': preferences
                    })
                )
        except Exception as ex:
            logger.exception(str(ex))
            print_exc()
            raise Http404

class RegistrationView(View):
    """ 
    Handle the HTTP requests related to registration 
        - GET: retrieve page 
        - POST: submit the information of the visitor user 
    """
    
    def get(self, request):
        """ Load the host/app/visitors/registration.html web page """
        try:
            assert isinstance(request, HttpRequest)

            # get list of countries
            import pycountry
            list = pycountry.countries
            result = []
            for i in list:
                result.append(i.name)

            # update operation between 2 integer
            from random import randint
            literal = str(randint(0,6))+ "+" + str(randint(0,4))
            
            return render(request,
                'app/visitors/registration.html',
                context_instance = RequestContext(request,
                {
                    'title': _('Registration page'),
                    'year':datetime.now().year,
                    'title': "AoD | " + _("Registration"),
                    'experience': ItExperience.objects.all().order_by('id'),
                    'CountriesList': result,
                    'categories': Categories.objects.all().order_by('id'),
                    'literal': literal
                }))
        except:
            print_exc()
            return server_error(request)

    def post(self, request):
        """ Submit and store the information of new user """

        # If the <request> is a HttpRequest object continue.  Else raise an
        # Exception
        assert isinstance(request, HttpRequest)

        # Registration process
        try:
            instance = json.loads(request.body)
            print instance

            # Create user instance
            dt = datetime.today()
            user = Users(name=instance['rg_name'], 
                lastname=instance['rg_lastname'],
                username=instance['rg_username'], 
                pwd=hashPassword(instance['rg_pwd']), 
                email=instance['rg_email'],
                mobile=instance['rg_mobile'], 
                country=instance['rg_country'], 
                is_active=False,         # for demo issues True
                experience=ItExperience.objects.get(pk=instance['rg_it_experience']), 
                last_login=dt,
                registration=dt)
            user.save()
            # get primary key
            _pk = user.id 
            
            # Create its role(s)
            rolesList = ["provider", "consumer", "carer"]
            for i in rolesList:
                if i in instance['rg_role']:
                    # cases
                    if i in ["Provider", "provider", "PROVIDER"]:
                        provider = Providers(user=Users.objects.get(pk=_pk), is_active=True, company=_("Not available"))
                        provider.save()
                    if i in ["Consumer", "consumer", "CONSUMER"]:
                        consumer = Consumers(user=Users.objects.get(pk=_pk), crowd_fund_notification=instance.get('crowd_notification', False), crowd_fund_participation=instance.get('crowd_participation', False), is_active=True)
                        consumer.save()
                    if i in ["Carer", "carer", "CARER"]:
                        carer = Carers(user=Users.objects.get(pk=_pk), is_active=True)
                        carer.save()
                else:
                    # cases
                    if i in ["Provider", "provider", "PROVIDER"]:
                        provider = Providers(user=Users.objects.get(pk=_pk), is_active=False, company=_("Not available"))
                        provider.save()
                    if i in ["Consumer", "consumer", "CONSUMER"]:
                        consumer = Consumers(user=Users.objects.get(pk=_pk), crowd_fund_notification=False, crowd_fund_participation=False, is_active=False)
                        consumer.save()
                    if i in ["Carer", "carer", "CARER"]:
                        carer = Carers(user=Users.objects.get(pk=_pk), is_active=False)
                        carer.save()
            
            # Associate user with desired categories/channels
            for i, v in enumerate(instance['rg_channels']):
                user.categories.add(v)

            subject = _("[P4ALL] AoD Registration")
            to = [user.email]
            domain = domainURL() 

            # create a hash for activation link
            hash = hashPassword(user.email)

            # send notification to activate his/her account
            body = "Dear "+str(user.name) +" " + str(user.lastname)+",\n\n"
            body += "Your registration was successfully completed in the AoDemand marketplace.\n"
            body += "The required username is: " + user.username+".\n"
            body += "Please follow the below link to activate your account:\n\n"
            body += domain + reverse('account_activation') + "?p="+ user.email +"&q="+ hash + "\n\n"
            body += "We don't check this mailbox, so please don't reply to this message.\n\n"
            body += "Sincerely,\nThe AoD administrator team"
            # send email
            sendEmail(to, subject, body, False)

            # server response in success
            return JsonResponse({"state": True, "redirect": reverse('account_success_registration')})
            
        except:  
            print_exc()
            # server response in failure
            return JsonResponse({"state": False})
  
def registrationSuccess(request,):
    """ Whether registration was successfully completed, redirect user """
    return render(request,
        'app/visitors/registration_success.html',
        context_instance = RequestContext(request,
        {
            'year':datetime.now().year,
            'username': _("user"),
            'title': _("AoD Registration")
        })) 

def hashPassword(password):
    """ Hash every password using SHA and SALT """
    try:
        import uuid
        import hashlib
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    except:
        pass    

def checkPassword(hashedPassword, typedPassword):
    import uuid
    import hashlib
    password, salt = hashedPassword.split(':')
    return password == hashlib.sha256(salt.encode() + typedPassword.encode()).hexdigest()

def accountActivation(request):
    """
    Activate an new account using email, value and checking the registration datetime 
    URL format: http://localhost:8000/account/activation?p={email}&q={hash}
    hash: the registration date/time in md5
    """
    try:
        assert isinstance(request, HttpRequest)

        if request.GET.get('p') == None:
            raise Exception("No valid email")
        if request.GET.get('q') ==None:
            raise Exception("No valid value")

        user = Users.objects.get(email=request.GET.get('p'))
        if user is None or user is list:
            raise Exception("Activation not success!")
        
        if checkPassword(request.GET.get('q'), request.GET.get('p')):
            # activate account
            Users.objects.filter(email=request.GET.get('p')).update(is_active=True)
            
            return render(request,
                'app/visitors/login.html',
                context_instance = RequestContext(request,
                {
                    'title':_('About'),
                    'message':"<center><span class='label label-primary' role='contentinfo'><i class='fa fa-info-circle fa-fw'></i>" + _("Your account was activated.") + "</span></center>",
                    'year': "" + datetime.now().year,
                }))
        raise Exception(_("Activation was expired.")) 
       
    except Exception as e:
        # handle any exception
        return render(request,
            'app/visitors/login.html',
            context_instance = RequestContext(request,
            {
                'title': _('About'),
                'message': "<center>"+str(e.args[0])+"</center>",
                'year': datetime.now().year,
            }))

    except:
        raise Exception(_("Activation was expired."))

class ForgotPasswordView(View):
    def get(self, request):
        """ Enter the email account """
        try:
            assert isinstance(request, HttpRequest)
            template = 'app/visitors/forgot-password.html'
            
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':_('Forgot password'),
                    'year':datetime.now().year,
                }))                
        except:
            raise Http404


#==============================
#   Authentication 
#==============================
def login(request):
    """Renders the login page."""

    try:
        assert isinstance(request, HttpRequest)
    
        if 'id' in request.session.keys() and 'username' in request.session.keys():
            #return redirect(reverse('landing_page'))
            return redirect(reverse('home_page'))

        return render(request,
            'app/visitors/login.html',
            context_instance = RequestContext(request,
            {
                'title': _('Login'),
                'message':None,
                'year':datetime.now().year,
            })
        )
    except:
        if settings.DEBUG:
            print_exc()
        return Http404

@require_http_methods(["POST"])
def loginAuth(request):

    try:
        assert isinstance(request, HttpRequest)
        request.session.flush()
    
        # import libs
        import uuid
        import hashlib
    
        if request.POST.get("username") != None:
            #_usr = request.POST.get("username")
            user = None
            user = Users.objects.get(username=request.POST.get("username"))
            if user is None or user.is_active == False:
                raise Exception("Username does not exist")

        if request.POST.get("pwd") != None:
            if checkPassword(user.pwd, request.POST.get("pwd")) == False:
                raise Exception("Password does not match")

        # session info
        request.session['id'] = user.id
        request.session['username'] = user.username
        request.session['cart'] = []
        # keep roles state - for future use
        request.session['is_provider']  = Providers.objects.get(user_id=user.id).is_active
        request.session['is_consumer']  = Consumers.objects.get(user_id=user.id).is_active
        request.session['is_carer']     = Carers.objects.get(user_id=user.id).is_active

        # generate paypal token if user->provider and e-shop has been registered
        retrieve_paypal_access_token(user.id)
        
        # move to his dashboard
        return redirect(reverse('home_page'))

    except Exception as e:
        logger.warn(str(e))
        # preview the following message on user
        message = "%s %s" % (_("Wrong combination of your credentials and your role"), _("Try again."))
        details = '<center><span class="label label-danger" role="contentinfo"><i class="fa fa-exclamation-circle fa-lg fa-fw"></i> ' + message + '</span></center><br>'
        
        return render(request,
            'app/visitors/login.html',
            context_instance = RequestContext(request,
            {
                'message': details,
                'year':datetime.now().year,
            })
        )
    except:
        raise Exception("server error")  

class Logout(View):
    
    def get(self, request):
        try:
            if 'id' in request.session.keys():
                userID = request.session['id']

                # Logout from Social Network
                if socialNetworkIntegration():
                    sn = socialnetwork.SocialNetwork()
                    state, response = sn.sessionLogout(userID)
                    if settings.DEBUG:
                        print state, response

            # Clear session values
            for i in request.session.keys():
                del request.session[i]
            request.session.flush()

            #response = redirect(reverse('landing_page'), permanent=False)
            response = redirect(reverse('home_page'), permanent=False)
            return response
        except Exception as ex:
            logger.critical(str(ex))
            if settings.DEBUG:
                print_exc()
            raise Http404


#==============================
#   User profile  & roles
#==============================
@loginRequiredView
class UploadUserMedia(View):
    def post(self, request, pk=None):
        """
        Update cover image of user
        """
        try:
            if request.is_ajax():
            
                try:
                    # store cover
                    if request.FILES['cover-img'] != None:
                        _image = request.FILES['cover-img']
                        temp = _image.name.split('.')
                        _image.name = str(pk) + "." + str(temp[-1])
                        path = settings.MEDIA_ROOT+ "/app/users/covers/" + _image.name
                        # remove file if exist
                        removeFileInExistance(path)
                        # store new file
                        storeFile(path, request.FILES['cover-img'])
                        # update instance
                        Users.objects.filter(pk=pk).update(cover=_image)
                except:
                    pass

                try:
                    # store logo
                    if request.FILES['logo'] != None:
                        _image = request.FILES['logo']
                        temp = _image.name.split('.')
                        _image.name = str(pk) + "." + str(temp[-1])
                        path = settings.MEDIA_ROOT+ "/app/users/logos/" + _image.name
                        # remove file if exist
                        removeFileInExistance(path)
                        # store new file
                        storeFile(path, request.FILES['logo'])
                        Users.objects.filter(pk=pk).update(logo=_image)
                except: 
                    pass
    
            return JsonResponse({'state': "OK"})
        except:
            return JsonResponse({'state': "ERROR"})

@loginRequiredView
class UserUpdatePersonalInfo(View):
    """
     Update user fields related to the personal information
    """
    
    # properties
    template = 'app/prosumers/profile/personal-info.html'

    # methods
    def post(self, request, pk=None):
        assert isinstance(request, HttpRequest)
    
        # check if AJAX request
        if request.is_ajax():
            try:
                # check the validity of ID
                offset = int(pk)
                # read JSON payload
                instance = json.loads(request.body)
                # update User instance
                Users.objects.filter(id=pk).update(name=instance["name"], lastname=instance["lastname"], country=instance["country"], 
                    city=instance["city"], address=instance["address"], postal_code=instance["postal_code"]
                )
            
                # load updated user instance
                user = Users.objects.get(pk=pk)
                error = False

                # get countries
                import pycountry
                list = pycountry.countries
                countries = []
                for i in list:
                    countries.append(i.name)
            
            except:
                user = None
                error = "The update of you personal information did not complete"

            # Server response
            return render(request, self.template,
                context_instance = RequestContext(request,
                {
                    'object': user,
                    'error': error,
                    'countryList': countries,
                    'logo': settings.MEDIA_URL + "app/users/logos/" + str(user.logo)
                }))
        else:
            # reload the page
            return consumer_profile(request, pk)  

@loginRequiredView
class UserUpdateContactInfo(View):
    """
    Update user fields related to the contact issues
    """
    
    # properties
    template = 'app/prosumers/profile/contact-info.html'

    # methods
    def post(self, request, pk=None):
        assert isinstance(request, HttpRequest)
    
        # check if AJAX request
        if request.is_ajax():
            try:
                # check the validity of ID
                offset = int(pk)
                # read JSON payload
                instance = json.loads(request.body)
                # update User instance
                Users.objects.filter(id=pk).update(email=instance["email"], mobile=instance["mobile"])
            
                # load updated user instance
                user = Users.objects.get(pk=pk)
                error = False          

            except:
                user = None
                error = "The update of your contact information did not complete"

            # Server response
            return render(request, self.template,
                context_instance = RequestContext(request,
                {
                    'object': user,
                    'error': error,
                    #'images': {'cover': {'exist': False, 'path': ''}, 'profile': {'exist': True, 'path': '../../../static/app/images/home/users/128.jpg'}}
                }))
        else:
            # reload the page
            return consumer_profile(request, pk)

@loginRequiredView
class UserUpdatePlatformInfo(View):
    """
    Update user fields related to the platform settings
    """
    # properties
    template = 'app/prosumers/profile/platform-info.html'
    
    # methods
    def post(self, request, pk=None):
        assert isinstance(request, HttpRequest)
    
        # check if AJAX request
        if request.is_ajax():
            try:
                # check the validity of ID
                offset = int(pk)
                error = False        
                # read JSON payload
                instance = json.loads(request.body)
                # update User instance
                Users.objects.filter(id=pk).update(experience=ItExperience.objects.get(pk=instance['skills']))

                # Update the roles of user
                rolesList = ["provider", "consumer", "carer"]
                if type(instance['roles']) is list:
                    for i in rolesList:
                        if i in instance['roles']:
                            if i in ["Provider", "provider", "PROVIDER"]:
                                provider = Providers.objects.filter(user_id=pk).update(is_active=True, company="N/A")
                            if i in ["Consumer", "consumer", "CONSUMER"]:
                                consumer = Consumers.objects.filter(user_id=pk).update(crowd_fund_notification=instance['crowd_notification'], crowd_fund_participation=instance['crowd_participation'], is_active=True)
                            if i in ["Carer", "carer", "CARER"]:
                                carer = Carers.objects.filter(user_id=pk).update(is_active=True)
                        else:
                            if i in ["Provider", "provider", "PROVIDER"]:
                                provider = Providers.objects.filter(user_id=pk).update(is_active=False)
                            if i in ["Consumer", "consumer", "CONSUMER"]:
                                consumer = Consumers.objects.filter(user_id=pk).update(is_active=False)
                            if i in ["Carer", "carer", "CARER"]:
                                carer = Carers.objects.filter(user_id=pk).update(is_active=False)

                # load updated user instance
                user = Users.objects.get(pk=pk)

                # Delete existing categories
                for i in Users.objects.get(pk=pk).categories.all():
                    user.categories.remove(i)
                # Create desired categories/channels of create
                if type(instance['categories']) is list:
                    for i, v in enumerate(instance['categories']):
                        user.categories.add(v)
            
                # load roles
                roles = []
                carer = Carers.objects.get(user_id=pk)
                roles.append({"role": "Carer", "exist":carer.is_active})
                consumer = Consumers.objects.get(user_id=pk)
                roles.append({"role": "Consumer", "exist":consumer.is_active, "crowd_fund_participation": consumer.crowd_fund_participation,"crowd_fund_notification": consumer.crowd_fund_notification})
                provider = Providers.objects.get(user_id=pk)
                roles.append({"role": "Provider", "exist":provider.is_active, "crowd_fund_participation": provider.crowd_fund_participation,"crowd_fund_notification": provider.crowd_fund_notification, "brand_name": provider.company})   

            except:
                user = None
                error = "The update of your contact information did not complete"

            # Server response
            return render(request, self.template,
                context_instance = RequestContext(request, 
                {
                    'object': user,
                    'error': error,
                    'experience': ItExperience.objects.all().order_by('id'),
                    'categories': Categories.objects.all().order_by('id'),
                    'roles': roles,
                    #'images': {'cover': {'exist': False, 'path': ''}, 'profile': {'exist': True, 'path': '../../../static/app/images/home/users/128.jpg'}}
                }))
        else:
            # reload the page
            return consumer_profile(request, pk)

@require_http_methods(["GET"])
def checkEmail(request, pk=None):
    """ Check if email account per user """

    assert isinstance(request, HttpRequest)
    emailLen = 0
    try: 
        offset = int(pk)

        if request.GET.get("value") is not None:
            is_unique = Users.objects.filter(email = request.GET.get("value")).count()
            is_yours = Users.objects.filter(pk=pk).filter(email = request.GET.get("value")).count()
            
            if is_unique > 0:
                if is_yours != 1:
                    emailLen = 1
            
    
        return JsonResponse({"result": emailLen})
    except:
        return JsonResponse({"result": emailLen})

@loginRequired
def index():
    """ Index page: initial page for registered users """
    pass

@loginRequired
def profile(request, username=None):
    """Renders the home page."""
    try:
        assert isinstance(request, HttpRequest)

        if username != request.session['username']:
             return render(request, 'app/errors/401.html',
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'object':customer,
                    'title': _('Bad request!'),
                }))

        template = 'app/prosumers/profile/index.html'
        pk = request.session['id']

        try:
            customer = Users.objects.get(username=username)
        except ValueError:
            raise Http404("Invalid URL")

        # TODO: call corresponding view
        import pycountry
        list = pycountry.countries
        countries = []
        for i in list:
            countries.append(i.name)
        # TODO: call corresponding view
        exp = ItExperience.objects.all().order_by('id')

        # retrieve roles
        roles = []
        carer = Carers.objects.get(user_id=pk)
        roles.append({"role": "Carer", "exist":carer.is_active})
        consumer = Consumers.objects.get(user_id=pk)
        roles.append({"role": "Consumer", "exist":consumer.is_active, "crowd_fund_participation": consumer.crowd_fund_participation,"crowd_fund_notification": consumer.crowd_fund_notification})
        provider = Providers.objects.get(user_id=pk)
        roles.append({"role": "Provider", "exist":provider.is_active, "crowd_fund_participation": provider.crowd_fund_participation,"crowd_fund_notification": provider.crowd_fund_notification, "brand_name": provider.company})


        return render(request, template,
            context_instance = RequestContext(request,
            {
                'year':datetime.now().year,
                'object':customer,
                'countryList': countries,
                'experience': exp,
                'categories': Categories.objects.all().order_by('id'),
                'roles': roles,
                'media_url': "/profile/media/" + str(pk),
                'error': False,
                'cover': settings.MEDIA_URL + "app/users/covers/" + str(customer.cover),
                'user_logo': settings.MEDIA_URL + "app/users/logos/" + str(customer.logo),   
                'readonly': settings.OPENAM_INTEGRATION
            }))
    except:
        raise Http404

def getConsumerInfo(request, userID=None):
    try:
        user        = Users.objects.get(pk = request.session['id'])
        if (userID != None):
            user    = Users.objects.get(pk = userID)
        role        = Consumers.objects.get(user_id = user.id)  
        return True, user, role
    except:
        from traceback import print_exc
        print_exc()
        return False, -1, -1 

def getProviderInfo(request, userID=None):
    try:
        user        = Users.objects.get(pk = request.session['id'])
        if (userID != None):
            user    = Users.objects.get(pk = userID)
        role        = Providers.objects.get(user_id = user.id)  
        return True, user, role
    except:
        from traceback import print_exc
        print_exc()
        return False, -1, -1 

def getCarerInfo(request, userID=None):
    try:
        user        = Users.objects.get(pk = request.session['id'])
        if (userID != None):
            user    = Users.objects.get(pk = userID)
        role        = Carers.objects.get(user_id = user.id)  
        return True, user, role
    except:
        from traceback import print_exc
        print_exc()
        return False, -1, -1 

class ItExperienceView(View):
    """ Handle the HTTP GET request: retrieve a list of available options """

    def get(self,request):
        """ Retrieve a list of available IT experience levels """
        assert isinstance(request, HttpRequest)
        try: 
            expList = ItExperience.objects.all().order_by('id')
            result = []
            for i in expList:
                result.append({"id":i.id, "level":i.level, "title":i.description})
            return JsonResponse({"results": result, "code": 200})
        except:
            return JsonResponse({"results": "", "code": 404})

class CountriesView(View):
    """ Handle the HTTP GET request: retrieve a list of countries """

    def get(self, request):
        """ Get a list of countries"""
        try:
            assert isinstance(request, HttpRequest)
            import pycountry
            list = pycountry.countries
            result = []
            for i in list:
                result.append({"id":i.alpha2, "name":i.name})
            return JsonResponse({"results": result, "code": 200})
        except:
            return JsonResponse({"results": "", "code": 500})

@require_http_methods(["GET"])
def usernameConstraints(request):
    """ Check username: unique constraint """

    assert isinstance(request, HttpRequest)
    usersLen = 0
    try: 
        if request.GET.get("value") is not None:
            usersLen = Users.objects.filter(username = request.GET.get("value")).count()
        return JsonResponse({"result": usersLen})
    except:
        return JsonResponse({"result": usersLen})

@require_http_methods(["GET"])
def emailConstraints(request):
    """ Check email: unique constraint """

    assert isinstance(request, HttpRequest)
    emailLen = 0
    try: 
        if request.GET.get("value") is not None:
            emailLen = Users.objects.filter(email = request.GET.get("value")).count()
        return JsonResponse({"result": emailLen})
    except:
        return JsonResponse({"result": emailLen})

@require_http_methods(["GET"])
def categories(request):
    """ Retrieve a question per category """
    try:
        assert isinstance(request, HttpRequest)
        categories = Categories.objects.all().order_by('id')
        result = []
        for i in categories:
            result.append({"id":i.id, "title": i.title, "question":i.question})
        return JsonResponse({"results": result, "code": 200})
    except:
        return JsonResponse({"results": "", "code": 404})


#==============================
#   Generic dashboard
#==============================
@loginRequiredView
class ServiceSearch(View):

    def get(self, request):
        """ Loads the page related to the service listing and searching"""
        try :
            assert isinstance(request, HttpRequest)
            pk = request.session['id']

            # Clarify cases regarding the customization status
            if settings.CUSTOMIZATION_PROCESS:
                template = "app/prosumers/dashboard/customizedIndex.html"

                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'year': datetime.now().year,
                        'userID': request.session['id'],
                        'sortby': request.GET.get('sortby'),
                        'technicalSupport': TechnicalSupport.objects.all().order_by('type'),
                        'help': Topic.objects.filter(visible=True).order_by('title'),
                        'services': Services.objects.filter(is_visible=True)
                    })
                )
            else:
                template = "app/prosumers/dashboard/index.html"

                providers = []
                for i in Providers.objects.filter(is_active=True):
                    user =  Users.objects.get(id=i.user_id)
                    providers.append({"id": i.id, "name": user.name, "lastname": user.lastname, "count": Services.objects.filter(owner_id=i.id).count()})

                types = list()
                for i in list(TYPE_CHOICES):
                    types.append({ "type" : str((i[1].split(" ")[0]).lower()), "alias": str(i[0].lower()), "count": Services.objects.filter(type=i[0]).count() })

                chargingModels = []
                for model in ChargingPolicies.objects.all().order_by("id"):
                    chargingModels.append({"id": model.id, "name":model.name, "servNo": Services.objects.filter(charging_policy_id=model.id).count() })

                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'year': datetime.now().year,
                        'userID': request.session['id'],
                        'providers': providers,
                        'types': types,
                        'chargingModels': chargingModels,
                        'sortby': request.GET.get('sortby'),
                    })
                )
        except: 
            if settings.DEBUG:
                print_exc()
            raise Http404

@loginRequiredView
class ServiceSearchResults(View):
    def post(self, request):
        """ Return the result of search """

        try :
            template = 'app/prosumers/provider-dashboard/services/services.html'

            if request.is_ajax():
                assert isinstance(request, HttpRequest)
                pk = request.session['id']
                # customer-user info        
                user = Users.objects.get(pk=pk)

                # search options
                payload = json.loads(request.body)

                ####################################
                ##  Searching
                ####################################
                s = Services.objects.all()

                # Owners filtering
                owners = None
                if type(payload['owners']) is list and len(payload['owners']):
                    s = s.filter(owner_id__in=payload['owners'])

                # Categories
                categories = None
                if type(payload['categories']) is list and len(payload['categories']):
                    s = s.filter(categories__pk__in=payload['categories'])

                # types
                types = None
                if type(payload['types']) is list and len(payload['types']):
                    types = payload['types']
                    for i, v in enumerate(types):
                        types[i]=v.upper()
                    s = s.filter(type__in=types)

                # pricing policies
                models = None
                #map: free->1, paid->0
                if type(payload['models']) is list and len(payload['models']):
                    if payload['models'] == [1]:
                        s = s.filter(charging_policy_id__in=payload['models'])
                    elif payload['models'] == [0]:
                        s = s.exclude(charging_policy_id__exact=1)
                        if payload["minPrice"] != "":
                            s = s.filter(price__gte=float(payload["minPrice"]))
                        if payload["maxPrice"] != "":
                            s = s.filter(price__lte=float(payload["maxPrice"]))

                # QoS
                minQoS, maxQoS = None, None
                if payload['minQoS'] != None:
                    minQoS = payload['minQoS']
                if payload['maxQoS'] != None:
                    maxQoS = payload['maxQoS']


                ####################################
                ##  Sorting and View
                ####################################
                # view
                view = 'm'
                
                if payload['view'] != None:
                    view = payload['view']
                
                # Sort services by user choice
                sortby = "title"
                
                if payload['sortby'] != None:
                    sortby = sortByMap(payload['sortby'])
                
                # Filter services per page
                limit = 30
                """
                if request.GET.get('limit') != None:
                    limit = sortByMap(request.GET.get('limit')) 
                """

                ####################################
                ##  Query
                ####################################
                # services
                servicesInfo = []

                servicesList = s.values_list('id', flat=True)
                uniqueServiceList = set(list(servicesList))
                s = Services.objects.filter(pk__in=uniqueServiceList)
                
                if payload["distance"] != "" and payload["lat"] !="" and payload["lon"] != "":
                    for service in s.order_by(sortby)[:limit]:
                        # check location
                        if service.location_constraint == True:
                            distance = getDistance(payload["lat"], payload["lon"], service.latitude, service.longitude)                        
                            if 0 <= float(distance) <= float(payload["distance"]): 
                            
                                # check QoS
                                rating = ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0]
                                reviews = ConsumersToServices.objects.filter(service_id=service.id).count()
                                
                                if minQoS != None and maxQoS != None: 
                                    if int(reviews) > 0 and float(minQoS) <= float(rating) <= float(maxQoS):
                                        servicesInfo.append({
                                            "id": service.id, 
                                            "title":service.title, 
                                            "description": service.description, 
                                            "price":service.price, 
                                            "unit":service.unit, 
                                            "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                                            "rating": rating, 
                                            "reviews": reviews, 
                                            "type": service.type,
                                            "logo": Users.objects.get(pk=service.owner_id).logo.name, 
                                            "image": settings.MEDIA_URL + settings.SERVICES_IMAGE_PATH + str(service.image)
                                        })
                                else:
                                    servicesInfo.append({
                                        "id": service.id, 
                                        "title":service.title, 
                                        "description": service.description, 
                                        "price":service.price, 
                                        "unit":service.unit, 
                                        "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                                        "rating": rating, 
                                        "reviews": reviews, 
                                        "type": service.type,
                                        "logo": Users.objects.get(pk=service.owner_id).logo.name, 
                                        "image": settings.MEDIA_URL + settings.SERVICES_IMAGE_PATH + str(service.image)
                                    })
                else:
                    for service in s.order_by(sortby)[:limit]:
                        # check QoS
                        rating = ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0]
                        reviews = ConsumersToServices.objects.filter(service_id=service.id).count()
                                
                        if minQoS != None and maxQoS != None:
                            if int(reviews) > 0 and float(minQoS) <= float(rating) <= float(maxQoS):
                                servicesInfo.append({
                                    "id": service.id, 
                                    "title":service.title, 
                                    "description": service.description, 
                                    "price":service.price, 
                                    "unit":service.unit, 
                                    "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                                    "rating": rating,
                                    "reviews": reviews, 
                                    "type": service.type,
                                    "logo": Users.objects.get(pk=service.owner_id).logo.name, 
                                    "image": settings.MEDIA_URL + settings.SERVICES_IMAGE_PATH + str(service.image)
                                })
                        else:
                            servicesInfo.append({
                                "id": service.id, 
                                "title":service.title, 
                                "description": service.description, 
                                "price":service.price, 
                                "unit":service.unit, 
                                "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                                "rating": rating, 
                                "reviews": reviews, 
                                "type": service.type,
                                "logo": Users.objects.get(pk=service.owner_id).logo.name, 
                                "image": settings.MEDIA_URL + settings.SERVICES_IMAGE_PATH + str(service.image)
                            })

                response_dic = {
                        'services': servicesInfo,
                        'sortby': sortby,
                        'view': view
                    }
                return render(request, template, response_dic)
            else:
                return JsonResponse({}, status=status.HTTP_200_OK)

        except AttributeError as at:
            raise Http404
        except:
            print_exc()
            raise Http404

def sortByMap(parameter):
    list = [{"parameter": "asc_title", "sortby": "title"}, 
            {"parameter": "desc_title", "sortby": "-title"}, 
            {"parameter": "asc_price", "sortby": "price"},
            {"parameter": "desc_price", "sortby": "-price"}
        ]

    for i,v in enumerate(list):
        if v["parameter"] == parameter:
            return v["sortby"]

#==============================
#   Provider dashboard
#==============================
@loginRequiredView
class ProviderServices(View):
    def get(self, request):
        """
        Get the list of offering services per provider
        """

        try:
            template = 'app/prosumers/provider-dashboard/index.html'

            user = Users.objects.get(pk=request.session['id'])
            _owner = Providers.objects.get(user_id=user.id)

            # Check if Social network integration
            integrationWithSocialNetwork = {
                "state": socialNetworkIntegration(),
                "url": settings.SOCIAL_NETWORK_WEB_SERVICES['base'] + settings.SOCIAL_NETWORK_WEB_SERVICES['services']['delete']
            }

            # check if provider has entered his paypal credentials
            provider = Providers.objects.get(user_id=request.session['id'])
            settings_existance = PaypalCredentials.objects.filter(provider=provider).count()

            services = Services.objects.exclude(type='C')

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'servicesTypes': {
                        'human': Services.objects.filter(type='H', owner=_owner.id).count(), 
                        'machine': Services.objects.filter(type='M', owner=_owner.id).count(),
                        'android': Services.objects.filter(type='A', owner=_owner.id).count(), 
                        'windows': Services.objects.filter(type='W', owner=_owner.id).count(), 
                        'ios': Services.objects.filter(type='I', owner=_owner.id).count(), 
                    },
                    'chargingModels': {
                        'free': services.exclude(type='C').filter(charging_policy=1, owner=_owner.id).count(),
                        'paid': services.exclude(type='C').exclude(charging_policy=1).filter(owner=_owner.id).count()
                    },
                    'locationLimitations': {
                        'with': services.exclude(type='C').filter(location_constraint=True,  owner=_owner.id).count(),
                        'without': services.exclude(type='C').filter(location_constraint=False,  owner=_owner.id).count()
                    },
                    'lingualLimitations': {
                        'with': services.exclude(type='C').filter(language_constraint=True,  owner=_owner.id).count(),
                        'without':services.exclude(type='C').filter(language_constraint=False,  owner=_owner.id).count()
                    },
                    'services': services.filter(owner=_owner.id),
                    "integrationWithSocialNetwork": integrationWithSocialNetwork,
                    "customizedVersion": settings.CUSTOMIZATION_PROCESS,
                    "settings_existance": settings_existance,
                })
            )
        except:
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

@loginRequiredView
class ServiceCreate(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ServiceCreate, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            import pycountry

            template = 'app/prosumers/provider-dashboard/services/registration/index.html'
            pk=request.session['id']
            user = Users.objects.get(pk=pk)
            provider = Providers.objects.get(user_id=pk)
            payment_settings_existance = PaypalCredentials.objects.filter(provider=provider).count()

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'types': TYPE_CHOICES,
                    'categories': Categories.objects.all().order_by('id'),
                    'charging_models': ChargingPolicies.objects.all(),
                    'currencies': pycountry.currencies,
                    'users': Users.objects.exclude(pk=pk).order_by('email'),
                    'languages': pycountry.languages,
                    'payment_settings_existance': payment_settings_existance,
                    'recurring_payment_frequency_choices': RECURRING_PAYMENT_FREQUENCY_CHOICES,
                    'recurring_payment_type_choices': RECURRING_PAYMENT_TYPE_CHOICES,
                    'frequency_interval_choices': FREQUENCY_INTERVAL_CHOICES,
                    'cycles_choices': CYCLES_CHOICES
                }))
    
        except:
            if settings.DEBUG:
                print_exc()
            return redirect(reverse('provider_dashboard'))

    def post(self, request):
        """
        Create a new service of a provider
        """

        try:
            from app.views.payment import retrieve_paypal_access_token

            pk = request.session['id']

            payload = json.loads(request.body)
            payload['owner'] = pk
            serializer = SimpleServiceSerializer(data=payload)
            if not serializer.is_valid():
                raise Exception(serializer.errors)
            if settings.DEBUG:
                print payload

            ## Create a new service
            #service = SimpleServiceSerializer(**payload)
            dt = datetime.today()
            service = Services(title=payload['title'], 
                description=payload['description'],
                version= payload['version'] if 'version' in payload else None,
                license=payload['license'] if 'license' in payload else None,
                type=payload["type"],
                charging_policy=ChargingPolicies.objects.get(pk=payload["charging_policy"]),
                owner=Providers.objects.get(user_id=payload['owner']),
                price=payload["price"],
                unit=payload["unit"],
                requirements=payload["requirements"] if "requirements" in payload else None,
                installation_guide=payload["installation_guide"] if "installation_guide" in payload else None,
                usage_guidelines=payload["usage_guidelines"] if 'usage_guidelines' in payload else None,
                is_public=payload["is_public"],
                constraints=payload["constraints"] if "constraints" in payload else None,
                language_constraint=payload["language_constraint"],
                location_constraint=payload["location_constraint"],
                latitude=payload["latitude"],
                longitude=payload["longitude"],
                skype=payload["skype"] if "skype" in payload else None,
                coverage=payload["coverage"],
                resource_link=payload.get("resource_link", None),
                is_visible= bool(int(payload["is_visible"])),
                community_support = bool(int(payload["community_support"])),
                modified_date=dt,
                created_date=dt
            )
            service.save()
            _service = service.id

            # Associate service with desired categories
            associateServiceCategories(payload['categories'], service)

            # keywords
            insertServiceKeywords(payload["keywords"], service.id)

            # languages
            if payload['language_constraint'] == True:
                insertServiceLanguages(payload["languages"], service.id)

            # if payment (sale/authorize)
            if service.charging_policy_id in [2,3]:
                servicePayment = ServicePayment(
                    service=Services.objects.get(pk=service.id), 
                    payment_type=payload['payment_type'],
                    tax=payload.get('tax', 0.0),
                    handling_fee=payload['handling_fee'],
                    shipping=payload.get('shipping', 0.0),
                    shipping_discount=payload['shipping_discount'],
                    insurance=payload['insurance']
                )
                servicePayment.save()
                logger.info("Store the service sale-payment details")

            elif service.charging_policy_id in [4,5,6,7]:
                # recurring payment
                recurring_payment = ServiceRecurringPayment.objects.create(
                    service=Services.objects.get(pk=service.id), 
                    rec_payment_type =payload.get('rec_payment_type'),
                    rec_payment_def_type=payload.get('rec_payment_def_type'),
                    frequency=get_subscription_period(service.charging_policy_id),
                    frequency_interval=payload.get('frequency_interval', 0),
                    cycles=payload.get('cycles', 0),
                    tax=payload.get('tax', 0.0),
                    shipping=payload.get('shipping', 0.0),
                    merchant_setup_fee=payload.get('merchant_preferences', 0.0),
                )

                # IAM - access token
                access_token = Tokens.objects.get(user_id=request.session['id']).access_token
          
                # Paypal - access token
                paypal_token = retrieve_paypal_access_token(service.owner.user.id)
                if paypal_token is None or paypal_token == "":
                    raise Exception("The Paypal token of the service provider is empty.")

                payload = {
                    "name": "Plan for the service {}".format(service.title),
                    "description": "Plan with {} payment type".format(recurring_payment.rec_payment_def_type),
                    "type": recurring_payment.rec_payment_type,
                    "payment_definitions": [
                        {
                            "name": "Regular Payment Definition",
                            "type": recurring_payment.rec_payment_def_type.upper(),
                            "frequency": recurring_payment.frequency.upper(),
                            "frequency_interval": str(recurring_payment.frequency_interval),
                            "amount": {
                                "value": service.price,
                                "currency": service.unit,
                            },
                            "cycles": "12",
                            "charge_models": [
                                {
                                    "type": "SHIPPING",
                                    "amount": {
                                        "value": recurring_payment.shipping,
                                        "currency": service.unit,
                                    }
                                },
                                {
                                    "type": "TAX",
                                    "amount": {
                                        "value": recurring_payment.tax,
                                        "currency": service.unit,
                                    }
                                }
                            ]
                        },
                    ],
                    "merchant_preferences": {
                        "setup_fee": {
                            "value": recurring_payment.merchant_setup_fee,
                            "currency": service.unit,
                        },
                        "return_url": domainURL() + reverse('execute_paypal_billing_agreement', kwargs={'pk': service.id}),
                        "cancel_url": domainURL() + reverse('skip_paypal_billing_agreement', kwargs={'pk': service.id}),
                        "auto_bill_amount": "YES",
                        "initial_fail_amount_action": "CONTINUE",
                        "max_fail_attempts": "0"
                    }
                }    

                # create and activate a billing plan
                billing_plan = p4a_payment.BillingPlan(access_token, paypal_token)
                (http_status, response_json) = billing_plan.create(payload)

                if int(http_status) in [200, 201]:
                    plan_id = response_json['plan']['id']
                    ServiceRecurringPayment.objects.filter(pk=recurring_payment.id).update(plan_id=plan_id)
                    (http_status, response_json) = billing_plan.activate(plan_id)
              
                logger.info("Store the service subscription details")

            response = {"id": _service, "success_url": reverse('provider_dashboard'), "media_url": reverse("upload_service_media", kwargs={'pk':_service}), "sn_integration": False}        
            # check social network integration status
            if socialNetworkIntegration():
                response['sn_integration'] = True
                response['sn_link'] = settings.SOCIAL_NETWORK_WEB_SERVICES['base'] + settings.SOCIAL_NETWORK_WEB_SERVICES['services']['insert'] + str(_service)
                response['auth_basic'] = settings.SOCIAL_NETWORK_WEB_SERVICES_AUTH
            return JsonResponse(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.critical(str(e))
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"reason": e.args}, status=status.HTTP_400_BAD_REQUEST)            
        except:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@loginRequiredView
class ServiceView(View):
    def get(self, request, pk=None):
        """ 
        Preview of the service for provider 
        """

        try:
            template = 'app/prosumers/provider-dashboard/services/item/preview/index.html'
            
            # service and provider info
            user = Users.objects.get(pk=request.session['id'])
            provider = Providers.objects.get(user_id=user.id)

            service = Services.objects.get(pk=pk)

            keywords = ServiceKeywords.objects.filter(service=service.id).all()
            languages = []
            import pycountry
            for lang in ServiceLanguages.objects.filter(service=service.id).all():
                for i in pycountry.languages:
                    if lang.alias == i.terminology:
                        languages.append(i.name)

            # fetch average value of metric per service
            avg_metrics_list = list()
            for metric in EvaluationMetric.objects.all():
                avg_metrics_dict = dict()
                avg_metrics_dict['name'] = metric.name
                avg_metrics_dict['score'] = ConsumerServiceEvaluation.objects.filter(service_id=service.id).\
                    filter(evaluation_metric_id=metric).aggregate(Avg('score')).values()[0]
                avg_metrics_list.append(avg_metrics_dict)            

            # fetch consumers/users
            service_has_used = ConsumersToServices.objects.filter(service_id=service.id)

            # Social network comp state
            integrationWithSocialNetwork = {
                "state": socialNetworkIntegration(),
                "url": settings.SOCIAL_NETWORK_WEB_SERVICES['base'] + settings.SOCIAL_NETWORK_WEB_SERVICES['services']['delete'] + str(service.id)
            }

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'service': service,
                    'keywords': keywords,
                    'categories': service.categories.all(),
                    'languages': languages,
                    "integrationWithSocialNetwork": integrationWithSocialNetwork,
                    'avg_metrics_list': avg_metrics_list,
                    'reviews': service_has_used.count(),
                    'reviewsList': service_has_used.exclude(review_date__isnull=True).order_by('-review_date'), 
                    'consumers': service_has_used,                 
                }))

        except Exception as ex:
            logger.exception(str(ex))
            return HttpResponseServerError(str(ex))

    def put(self, request, pk=None):
        """ 
        Update an existing service
        """
        try:
            assert isinstance(request, HttpRequest)
            user_id = request.session['id']

            if pk == None:
                raise Exception("Invalid pk")

            payload = json.loads(request.body)
            payload['owner'] = user_id
            serializer = SimpleServiceSerializer(data=payload)
            if not serializer.is_valid():
                raise Exception(serializer.errors)
            if settings.DEBUG:
                print payload

            # Update service
            Services.objects.filter(pk=pk).update(
                title=payload['title'], 
                description=payload['description'],
                version= payload['version'] if 'version' in payload else None,
                license=payload['license'] if 'license' in payload else None,
                type=payload["type"],
                charging_policy=ChargingPolicies.objects.get(pk=payload["charging_policy"]),
                price=payload["price"],
                unit=payload["unit"],
                requirements=payload["requirements"] if "requirements" in payload else None,
                installation_guide=payload["installation_guide"] if "installation_guide" in payload else None,
                usage_guidelines=payload["usage_guidelines"] if 'usage_guidelines' in payload else None,
                is_public=payload["is_public"],
                constraints=payload["constraints"] if "constraints" in payload else None,
                language_constraint=payload["language_constraint"],
                location_constraint=payload["location_constraint"],
                latitude=payload["latitude"],
                longitude=payload["longitude"],
                skype=payload["skype"] if "skype" in payload else None,
                coverage=payload["coverage"],
                resource_link=payload.get("resource_link", None),
                community_support = bool(int(payload["community_support"])),
                is_visible=bool(int(payload["is_visible"])),
                modified_date=datetime.today()
            )
            service = Services.objects.get(pk=pk)

            # Delete existing categories
            for i in service.categories.all():
                service.categories.remove(i)
            # Create relationships
            associateServiceCategories(payload['categories'], service)

            # Delete existing keywords
            ServiceKeywords.objects.filter(service_id=service.id).delete()
            # Insert new keywords
            insertServiceKeywords(payload["keywords"], service.id)

            ## Update languages
            ServiceLanguages.objects.filter(service_id=service.id).delete()
            if payload['language_constraint'] == True:
                insertServiceLanguages(payload["languages"], service.id)

            # Update the existing community or initiate new one
            communities = Community.objects.filter(service_id = service.id)
            if service.type == "C":
                if communities.count() == 0:
                    # insert community
                    community = Community(service_id = service.id, is_active = service.community_support)
                    community.save()
                    # insert owner
                    com_member = CommunityMember(
                        community_id = community.id,
                        user_id = request.session['id'],
                        is_owner = True,
                        is_active = True
                    )
                    com_member.save()

                    # Send email notifications towards admin
                    content = _("Dear admin,\n\nA new community has been initiated for the service %s.\n\nBest regards,%s\n")\
                         % (service.title, request.session['username'])
                    sendEmail([settings.DEVELOPER_EMAIL], _("[P4ALL] Community notification"), content, False)

                    # Send email notifications towards users (volunteers or professionals)
                    content = _("Dear community,\n\nA new community has been initiated for the service %s.\n\nBest regards,%s\n")\
                         % (service.title, request.session['username'])
                    email_list = Users.objects.filter(Q(is_volunteer=True) | Q(is_professional=True)).values_list('email', flat=True)
                    sendEmail(email_list, _("[P4ALL] Community notification"), content, False)
                else:
                    communities.update(is_active = service.community_support)
            else:
                if communities.count() == 0:
                    pass
                else:
                    # deactivate existing community
                    communities.update(is_active = False)

                    # Send email notifications towards admin
                    content = _("Dear admin,\n\nthe community for the service %s has disabled.\n\nBest regards,%s\n")\
                         % (service.title, request.session['username'])
                    sendEmail([settings.DEVELOPER_EMAIL], _("[P4ALL] Community notification"), content, False)

                    # Send email notifications towards registered community members
                    content = _("Dear community,\n\nA new community for the service %s has disabled.\n\nBest regards,%s\n")\
                         % (service.title, request.session['username'])
                    users_list = CommunityMember.objects.filter(community_id=communities[0].id).values_list('user_id', flat=True)
                    email_list = Users.objects.filter(id__in=users_list).values_list('email', flat=True)
                    sendEmail(email_list, _("[P4ALL] Community notification"), content, False)

            response = {"id": service.id, "success_url": reverse('provider_dashboard'), "media_url": reverse("upload_service_media", kwargs={'pk': service.id}), "sn_integration": False}
            return JsonResponse(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            print_exc()
            return JsonResponse(data={"reason": e.args, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None):
        """ 
        Delete a service based on service pk 
        """
        try:
            # check request type
            assert isinstance(request, HttpRequest)
            # check if id exist
            if pk == None:
                raise Exception("Invalid service pk")

            # check owner and provider role
            service = Services.objects.get(pk=pk)
            #if request.session['id'] != service.owner:
            #    raise Exception("403")
            
            # delete keywords instances         
            ServiceKeywords.objects.filter(service__exact=service.id).delete()
            # delete languages instances
            ServiceLanguages.objects.filter(service__exact=service.id).delete()

            # delete categories link
            for category in service.categories.all():
                service.categories.remove(category)

            # Send email notifications towards registered community members
            communities = Community.objects.filter(ref_service_id=service.id)
            if communities.count():
                community_owner = CommunityMember.objects.get(community_id=communities[0].id, is_owner=True)
                owner_profile = Users.objects.get(pk=community_owner.user_id)
                content = _("Dear %s,\n\nThe service %s that your community supports has removed. Please inform your members.\n\nThank you,\n%s")\
                    % (owner_profile.username, service.title, request.session['username'])
                sendEmail([owner_profile.email], _("[P4ALL] Community notification"), content, False)

            # remove instance
            try:
                service.delete()
            except ObjectDoesNotExist as ex:
                raise Exception(ex.args[0])
            return JsonResponse({"redirect": reverse("provider_dashboard"), "auth_basic": settings.SOCIAL_NETWORK_WEB_SERVICES_AUTH}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.critical(str(e))
            if settings.DEBUG:
                print_exc()
            return JsonResponse({"reason": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except:
            if settings.DEBUG:
                print_exc()
            return JsonResponse({"state": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@loginRequiredView
class ServiceUpdateView(View):
    def get(self, request, pk=None):
        """
        Load the HTML template for service modification
        """
        try:
            import pycountry
            template = 'app/prosumers/provider-dashboard/services/item/update/index.html'

            # service and provider info
            user_id = request.session['id']
            provider = Providers.objects.get(user_id=user_id)
            service = Services.objects.get(pk=pk)

            # load template
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'service': service,
                    'types': TYPE_CHOICES,
                    'categories': Categories.objects.all().order_by('id'),
                    'charging_models': ChargingPolicies.objects.all(),
                    'currencies': pycountry.currencies,
                    'users': Users.objects.exclude(pk=user_id).order_by('email'),
                    'languages': pycountry.languages,
                    'keywords': ServiceKeywords.objects.filter(service=service.id),
                    'recurring_payment_frequency_choices': RECURRING_PAYMENT_FREQUENCY_CHOICES,
                    'recurring_payment_type_choices': RECURRING_PAYMENT_TYPE_CHOICES,
                    'frequency_interval_choices': FREQUENCY_INTERVAL_CHOICES,
                    'cycles_choices': CYCLES_CHOICES                    
                }))
        except: 
            if settings.DEBUG:
                print_exc()
            raise Http404

@loginRequiredView
class UploadServiceMedia(View):

    def post(self, request, pk=None):
        """
        Upload files related to a service such as:
        the cover image, the logo and the software package
        """

        try:  
            try:
                if request.FILES['image']:
                    # store image
                    _image = request.FILES['image']
                    temp = _image.name.split('.')
                    _image.name = str(pk) + "." + str(temp[-1])
                    path = settings.MEDIA_ROOT+ "/app/services/images/" + _image.name
                    # remove file if exist
                    removeFileInExistance(path)
                    # store new file
                    storeFile(path, request.FILES['image'])
                    Services.objects.filter(pk=pk).update( image = _image)
            except:
                raise Exception("Image has not uploaded")

            #temp, path = None, None
            #try:
            #    if request.FILES['software']:
            #        # store cover
            #        _sw = request.FILES['srv_software']
            #        temp = _sw.name.split('.')
            #        _sw.name = str(pk) + "." + str(temp[-1])
            #        path = settings.MEDIA_ROOT+ "/app/services/packages/" + _sw.name
            #        # remove file if exist
            #        removeFileInExistance(path)
            #        # store new file
            #        storeFile(path, request.FILES['srv_software'])
            #        Services.objects.filter(pk=pk).update(software = _sw )
            #except:
            #    raise Exception("Spftware package has not uploaded")

            return JsonResponse(data={"image": path, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            return JsonResponse(data={"reason": str(e), "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)            
        except:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def associateServiceCategories(categories, service):
    """
    Create relationships among service and categories
    """
    try:
        if type(categories) == list:
            for i, v in enumerate(categories):
                service.categories.add(v)
        elif type(categories) in [str, int]:
            service.categories.add(v)
        else:
            return JsonResponse(data={"reason": _("Categories input neither list nor string/integer"), "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except :
        print_exc()

def insertServiceKeywords(keywords, service_id):
    """
    Create relationships among service and keywords
    """
    try:
        import re
        pattern = re.compile(r"[,;]")

        if keywords[-1] == ',':
           keywords = keywords[0:len(keywords)]
        keywords = pattern.split(keywords)
        if type(keywords) == list:
            for i in keywords:
                if i not in [None, "", " "]:
                    k = ServiceKeywords(service=Services.objects.get(pk=service_id), title=i)
                    k.save()
        elif type(keywords) is str:
            k = ServiceKeywords(service=Services.objects.get(pk=service_id), title=i)
            k.save()
    except:
        print_exc()

def insertServiceLanguages(languages, service_id):
    """
    Create relationships among service and supported languages
    """
    try:
        if type(languages) == list:
            for i in languages:
                if i is not None:
                    l = ServiceLanguages(service=Services.objects.get(pk=service_id), alias=i)
                    l.save()
        elif type(languages) is str and not None:
            l = ServiceLanguages(service=Services.objects.get(pk=service_id), alias=i)
            l.save()
    except:
        print_exc()

@loginRequiredView
class ServiceTechnicalMaterialListView(View):

    def get(self, request, pk):
        """Retrieve list of technical materials for a service

           pk: service ID
        """
        try:
            template = "app/prosumers/provider-dashboard/services/technical-support/index.html"
            service = Services.objects.get(pk=pk)
            serviceTechnicalSupportList = ServicesToTechnicalSupport.objects.filter(service_id=pk).order_by('id')
            technicalSupportList = TechnicalSupport.objects.all()

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'service': service,
                    'technicalSupportList': technicalSupportList,
                    'serviceTechnicalSupportList': serviceTechnicalSupportList,
                }))
        except:
            print_exc()
            raise Http404

    def post(self, request, pk):
        """Register a technical material for a service
           
           pk: service ID
        """
        try:
            if request.is_ajax():
                payload = json.loads(request.body)
                # Check if upload file or insert link
                uploadFile = False if int(payload['technical_support']) in [1, 4] else True
                payload['visible'] = True if "visible" in payload and payload['visible'] == "on" else False
                if int(payload['technical_support']) == 1:
                    payload['link'] = "https://www.youtube.com/embed/" + payload['link']

                serializer = SimpleServiceTechnicalSupportSerializer(data=payload)
                if serializer.is_valid():
                    material = serializer.save()
                    return JsonResponse({"id": material.id, "uploadFile": uploadFile, "uploadMediaURL": reverse('upload_service_technical_material', kwargs={'pk': pk, 'material':material.id})}, status=status.HTTP_201_CREATED)
                else:
                    print serializer.errors
                    return JsonResponse({"reason": str(serializer.errors), "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            return redirect(reverse('service_technical_materials', kwargs={'pk':pk}))
        except:
            print_exc()
            return JsonResponse({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@loginRequiredView
class UploadServiceTechnicalMaterialView(View):
        
    def post(self, request, pk, material):
        """Upload the file of a service's technical material"""
        try:
            if request.is_ajax():
                if settings.DEBUG:
                    print request.FILES

                if 'material' in request.FILES:
                    file = request.FILES['material']
                    extension = file.name.split(".")[-1]
                    lowerExtension = extension.lower()
                    filename = file.name.replace(" ", "_")

                    # File system path
                    TODAY_PATH = str(date.today().strftime("%Y/%m/%d/"))
                    FS_PATH_PREFIX = settings.MEDIA_ROOT + "/" + settings.SERVICES_TECHNICAL_SUPPORT + TODAY_PATH 
                    FS_PATH = FS_PATH_PREFIX + filename

                    # Overwrite if file exists
                    mkdir(FS_PATH_PREFIX)
                    removeFileInExistance(FS_PATH)
                    storeFile(FS_PATH, request.FILES['material'])

                    # URL path
                    path = settings.MEDIA_URL + settings.SERVICES_TECHNICAL_SUPPORT + TODAY_PATH + filename
                    ServicesToTechnicalSupport.objects.filter(pk=material).update(path=path, extension=extension)
                    return JsonResponse({}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"reason": "File with name material not found!", "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Skip it and reload list of materials
                return redirect(reverse('service_technical_materials', kwargs={"pk": int(pk)}))
        except:
            if settings.DEBUG:
                print_exc()
            return JsonResponse({"status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@loginRequiredView
class ServiceTechnicalMaterialObjectView(View):

    def delete(self, request, pk):
        """Delete a technical material of a service"""
        try:
            material = ServicesToTechnicalSupport.objects.get(pk=pk)
            FS_PATH = FS_PATH_PREFIX = settings.MEDIA_ROOT + material.path.replace('/media', '')
            removeFileInExistance(FS_PATH)
            material.delete()
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
        except:     
            print_exc()
            return JsonResponse({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def mkdir(path):
    """Create directory if not exists"""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError, e:
        print e

def storeFile(path, filename):
    """Create file in specific directory"""
    try:
        with open(path, 'wb+') as destination:
            for chunk in filename.chunks():
                destination.write(chunk)

        destination.close()
    except EnvironmentError, env:
        print env
        logger.error(env)
    except:
        logger.error("File not found")
        print_exc()

def removeFileInExistance(filepath):
    """Remove a file in specific path (if exist)"""
    try:
        os.remove(filepath)
    except OSError as e:
        print e
    except: 
        print_exc()

@loginRequiredView
class DetectBrokenLinks(View):

    def get(self, request):
        """Validate or not a registered link"""
        try:
            import requests
            if request.is_ajax():
                link = request.GET.get('link')
                if settings.DEBUG:
                    print link
                
                connection = requests.head(link)
                if int(connection.status_code) < 400:
                   return JsonResponse({}, status=status.HTTP_200_OK)
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        except Exception, ex:
            print_exc()
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

#===================================
#   Consumer dashboard
#===================================
@loginRequiredView
class ConsumerDashboard(View):
    def get(self, request):
        """
        Retrieve your personal cart 
        """
        
        template = "app/prosumers/consumer-dashboard/index.html" 
        try:
            # get ConsumerID
            state, user, consumer = getConsumerInfo(request)

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('My collection'),
                    'year':datetime.now().year,
                    'consumer': {"id": consumer.id, "info": user.name + " " + user.lastname}
                })
            )
        except:
            raise Http404

class ServiceConsumerView(View):

    def get(self, request, pk=None):
        """Render the service based on the user. The template is adjusted according to the user activity.

        The `purchased_date` means the date that the user was started to use the service (after payment proccess).
        The `end_date` means the date the user can not access the service and its resources (file or link).
        Among `purchased_date` and `end_date`, the user can access the service resources.

        In case free or one-off payment, one entry will be in the ConsumersToServices model.
        In case of pay per use or subscription services, multiple entries will be in the ConsumersToServices model.

        To decide if the user can access the resources or should purchase again the service, check if the `end_date` is None and the state of the flag `access_resource`.

        Any user can review a service once, if at least a entry exists in the ConsumersToServices model. 
        The review will be associated with the latest ConsumersToServices entry.
        """
        try:
            template = 'app/prosumers/search/services/preview.html'
            import pycountry

            # service and provider info
            service = Services.objects.get(pk=pk)
            charging_policy = ChargingPolicies.objects.get(pk=service.charging_policy.id)
            provider = Providers.objects.get(pk=service.owner_id)
            owner = Users.objects.get(pk=provider.user_id)
            # service types
            types = TYPE_CHOICES
            
            is_provider = False
            is_service_used = False
            permision_to_review = True
            permission_to_access_resource = False
            is_try_different_visible = False
            has_download_resource = 0

            if 'id' in request.session: 
                user_id = request.session['id']
                consumer = Consumers.objects.get(user_id=user_id)
                consumer_use_service = ConsumersToServices.objects.filter(consumer=consumer, service_id=pk)

                # Decide if user can review the service
                # Note: Provider can not review the service that owns
                if provider.user_id == user_id:
                    permision_to_review = False
                    is_provider = True
                else:
                    # Check if user uses or has purchased the service at least once
                    if consumer_use_service.count() > 0: 
                        # Check if user has already performed a review for the service directly
                        is_service_used = True
                        reviews_number = consumer_use_service.filter(rating__isnull=False).count()
                        if reviews_number > 0: 
                            permision_to_review = False
                    else:
                        permision_to_review = False

                # Decide usage or payment actions, access to resources
                if consumer_use_service.filter(end_date__isnull=True, access_resource=True).count() > 0: 
                    has_download_resource = consumer_use_service.filter(end_date__isnull=True, access_resource=True).first().download

                if charging_policy.id == 2:
                    # pay per use - access resource for 15 minutes
                    usages = consumer_use_service.filter(access_resource=True)
                    if usages.count():
                        end_date = usages.order_by('-purchased_date').first().end_date
                        d1 = datetime.utcnow().replace(tzinfo=None)  
                        d2 = end_date.replace(tzinfo=None)               
                        if 0 < datetime_diff_minutes(d1, d2) < 15.0:
                            permission_to_access_resource = True
                else:
                    permission_to_access_resource = consumer_use_service.filter(end_date__isnull=True, access_resource=True).count()       

                # Display or not the try different button
                if TrackUserSearch.objects.filter(user_id=request.session['id']).count():
                    is_try_different_visible = True
            else: 
                permision_to_review = False

            keywords = ServiceKeywords.objects.filter(service_id=service.id)
            if not keywords:
                keywords = None

            availableLanguages = ServiceLanguages.objects.filter(service_id=service.id).values_list('alias', flat=True)
            langList = compareLanguages(availableLanguages)
            
            community = None
            community_members = None
            community_volunteers = None
            community_professionals = None
            community_link = ""

            if service.type == 'C':
                # find members (volunteers & professionals) of community-based-service
                communities =  Community.objects.filter(service_id=pk)
                community = communities[0]
                community_members = CommunityMember.objects.filter(community_id=community.id, is_active=True)
                community_volunteers = community_members.filter(is_volunteer=True)
                community_professionals = community_members.filter(is_professional=True)
                community_members = community_members.values_list('user_id', flat=True)
            else:
                communities = Community.objects.filter(ref_service_id=pk)

            if communities.count():
                community = communities[0]
                community_link = reverse('service_view_page', kwargs={'pk': community.service.id})

            service_has_used = ConsumersToServices.objects.filter(service_id=service.id)

            # fetch average value of metric per service
            avg_metrics_list = list()
            for metric in EvaluationMetric.objects.all():
                avg_metrics_dict = dict()
                avg_metrics_dict['name'] = metric.name
                avg_metrics_dict['score'] = ConsumerServiceEvaluation.objects.filter(service_id=service.id).\
                    filter(evaluation_metric_id=metric).aggregate(Avg('score')).values()[0]
                avg_metrics_list.append(avg_metrics_dict)

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'service': service,
                    'provider': owner, 
                    'keywords': keywords,
                    'availableLanguages': langList,
                    'categories': Categories.objects.all().order_by('id'),
                    'model': ChargingPolicies.objects.get(pk=service.charging_policy_id),
                    'rating': service_has_used.aggregate(Avg('rating')).values()[0],
                    'reviews': service_has_used.count(),
                    'reviewsList': service_has_used.exclude(review_date__isnull=True).order_by('-review_date'),
                    'evaluation_metrics': EvaluationMetric.objects.filter(is_active=True),
                    'avg_metrics_list': avg_metrics_list,
                    'currencies': pycountry.currencies,
                    'technicalSupportList': ServicesToTechnicalSupport.objects.filter(service_id=pk, visible=True),
                    'community_members': community_members,
                    'community_volunteers': community_volunteers,
                    'community_professionals': community_professionals,
                    'community': community,
                    'community_link': community_link,
                    'permision_to_review': permision_to_review,
                    'is_provider': is_provider,
                    'is_service_used': is_service_used,
                    'permission_to_access_resource': permission_to_access_resource,
                    'paypal_logo': settings.PAYPAL_LOGO,
                    'paypal_buy_now': settings.PAYPAL_BUY_NOW_IMG,
                    'paypal_subscribe': settings.PAYPAL_SUBSCRIBE_IMG,
                    'paypal_unsubscribe': settings.PAYPAL_UNSUBSCRIBE_IMG,
                    'is_try_different_visible': is_try_different_visible,
                    'has_download_resource': has_download_resource
                })
            )
        except Exception as ex:
            logger.exception(str(ex))
            if settings.DEBUG: 
                print_exc()
            raise Http404

@loginRequiredView
class CartView(View):
    def get(self, request):
        """
        Retrieve your personal cart 
        """
        
        template = "app/prosumers/consumer-dashboard/cart/index.html" 
        try:
            services = None
            providers = []
            if 'cart' in request.session:
                list = request.session["cart"]       
                services = Services.objects.filter(pk__in=list)
                for s in services:
                    u = Users.objects.get(pk=s.owner_id)
                    providers.append({'service': s.id, "owner": u.name + " " + u.lastname })

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('My cart'),
                    'year':datetime.now().year,
                    'services': services,
                    'providers': providers,
                    'total': services.aggregate(Sum('price'))["price__sum"]
                }))
        except:
            raise Http404

    def post(self, request, service_pk):
        """
        Update your personal cart
        """
        try:

            if request.is_ajax:
                if 'cart' not in request.session:
                    cartList = []
                    cartList.append(service_pk)
                    request.session["cart"] = cartList
                else:
                    cart = request.session["cart"]
                    if service_pk not in cart:
                        cart.append(service_pk)
                        request.session["cart"] = cart
            else:
                raise Exception("No ajax")    
            return JsonResponse({"state" : 1})
        except Exception as ex:
            return JsonResponse({"state" : -1})
        except:
            return JsonResponse({"state" : 0})

    def delete(self, request, service_pk):
        """
        Remove item from your personal cart
        """
        try:

            if request.is_ajax:
                if 'cart' in request.session:
                    cart = request.session["cart"]
                    if service_pk in cart:
                        cart.remove(service_pk)
                        request.session["cart"] = cart
            else:
                raise Exception("No ajax")    
            return JsonResponse({"state" : 1})
        except Exception as ex:
            return JsonResponse({"state" : -1})
        except:
            return JsonResponse({"state" : 0})


#===================================
#   Network of assistance services
#   Carer dashboard
#===================================
@loginRequiredView
class NetworkAssistanceServicesRequests(View):
    def get(self, request):
        """Load the page that includes the NAS requests"""

        template = "app/carer-dashboard/index.html" 

        try:
            #load user ID
            pk = request.session['id']

            # load carer role
            state1, carProfile, carer = getCarerInfo(request)
            carerRequestData = []
            if request.session['is_carer']:
                carerRecords = CarersAssistConsumers.objects.filter(carer_id=carer.id)
                
                for obj in carerRecords:                    
                    consumer = Consumers.objects.get(pk=obj.consumer_id)
                    user = Users.objects.get(pk=consumer.user_id)
                    carerRequestData.append({
                        "id": str(obj.id),
                        "consumer_id": user.id, 
                        "name": user.name, 
                        "lastname": user.lastname, 
                        "response": obj.response,
                        "state": obj.state,
                        "created_at": obj.created_at,
                        "updated_at": obj.updated_at
                    })

            # load consumer role
            state1, conProfile, consumer = getConsumerInfo(request)
            consumerRequestData = []
            if request.session['is_consumer']:
                #consumer = Consumers.objects.get(user_id=pk)
                consumerRecords = CarersAssistConsumers.objects.filter(consumer_id=consumer.id)

                for obj in consumerRecords:                    
                    carer = Carers.objects.get(pk=obj.carer_id)
                    user = Users.objects.get(pk=carer.user_id)
                    consumerRequestData.append({
                        "id": str(obj.id),
                        "carer_id": user.id, 
                        "name": user.name, 
                        "lastname": user.lastname, 
                        "response": obj.response,
                        "state": obj.state,
                        "created_at": obj.created_at,
                        "updated_at": obj.updated_at
                    })

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Network of assistance services'),
                    'year': str(datetime.now().year),
                    'is_carer': request.session['is_carer'],
                    'carer_requests': carerRequestData,
                    'is_consumer': request.session['is_consumer'],
                    'consumer_requests': consumerRequestData
                }))
        except:
            raise Http404

@loginRequiredView
class NetworkAssistanceServicesCreateRequest(View):
    
    def get(self, request):
        """ 
        Load the web page to send a new request to assist a consumer with disability
        """

        template = "app/carer-dashboard/requests/create-new.html" 
        try:
            #load user
            pk = request.session['id']            

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Network of assistance services'),
                    'year': str(datetime.now().year),
                }))
        except:
            raise Http404

    def post(self, request):
        """
        Send a email/notification in which an authenticated user/carer request permissions to setup a 
        network of assistance services on behalf a user with disability.
        """

        try:
            # load json data
            instance = json.loads(request.body)
            consumerID = int(instance['consumer_id'])

            carer = Carers.objects.get(user_id = request.session['id'])
            consumer = Consumers.objects.get(user_id = consumerID)

            # insert record
            dt = datetime.now()
            nasRequest = CarersAssistConsumers(
                carer_id=carer.id,
                consumer_id=consumer.id,                
                created_at=dt
            )
            nasRequest.save()

            sender = Users.objects.get(pk=request.session['id'])
            receiver = Users.objects.get(pk=consumerID)

            # send notification to activate his/her account
            subject = "[P4ALL] Network of assistance services notification"
            
            if settings.DEBUG:
                to = settings.RECEIVER_EMAIL
            else:
                to = [receiver.email]

            # Create agree/disagree links
            path = domainURL() + reverse('guided_assistance_reply_to_request')
            positiveLink = path + "?rec=" + str(receiver.email) + "&sen=" + str(sender.email) + "&val=" + str(nasRequest.id) + "&code=true"
            negativeLink = path + "?rec=" + str(receiver.email) + "&sen=" + str(sender.email) + "&val=" + str(nasRequest.id) + "&code=false"

            body = "<div>Dear <strong>" + receiver.name + " " + receiver.lastname + "</strong>,<br><br>"
            body += "The authorized AoD user, " + sender.name + " " + sender.lastname + ", requires privileges to setup your personal network of assistance services!<br>"
            body += "Do you want to grant permission on him/her?<br><br>"
            body += "If you agree, click here: <a href='" + positiveLink + " '>Yes, I do!</a><br><br>"
            body += "Otherwise, click here: <a href='"+negativeLink+"'>No, I do not agree</a><br><br>"
            body += "Sincerely,<br>The AoD administration team</div>"

            # send email with HTML code
            sendEmail(to, subject, body, True)
            return JsonResponse({"state": True})
        except:
            from traceback import print_exc
            print_exc()
            return JsonResponse({"state": False})

class NetworkAssistanceServicesReplyRequest(View):
    def get(self, request):
        """
        Write the reply of each consumer in carer request
        """
        try:
            carerEmail      = request.GET.get('sen')
            receiverEmail   = request.GET.get('rec')
            requestID       = request.GET.get('val')
            state           = True if request.GET.get('code') in ["true", True] else False
            
            if carerEmail and receiverEmail and requestID:
                carer     = Users.objects.get(email=carerEmail)
                consumer  = Users.objects.get(email=receiverEmail)
                
                CarersAssistConsumers.objects.filter(id=requestID, carer_id=Carers.objects.get(user_id=carer.id).id, consumer_id=Consumers.objects.get(user_id=consumer.id).id).update(response=True, state=state, updated_at=datetime.now())

                subject = "[P4ALL] Network of assistance services notification"
                to = settings.RECEIVER_EMAIL if settings.DEBUG == True else [carer.email]
                
                # Inform the carer the consumer has replied on his/her request
                body = "<div>Dear <strong>" + carer.name + " " + carer.lastname + "</strong>,<br><br>"
                body += "The registered in AoD user, " + consumer.name + " " + consumer.lastname + ","
                if state == True:
                    body +=  " granted you with permission to setup his/her personal network of assistance services.<br>"
                else: 
                    body +=  " declined your request to setup his/her personal network of assistance services.<br>"
                body += "<br>Regards,<br>The AoD administration team</div>"

                # send email with HTML code
                sendEmail(to, subject, body, True)
                return redirect(reverse('guided_assistance_landing_page'))

        except ObjectDoesNotExist:
            print("Model does not exist")
            return Http404
        except MultipleObjectsReturned:
            print("Multiple instances founded")
            return Http404
        except:
            print_exc()
            return Http404

@loginRequiredView
class NetworkAssistanceServicesInviteCarers(View):

    def get(self, request):
        """ 
        Load the web page to send a new invitation on a carer
        """

        template = "app/carer-dashboard/invitations/index.html" 
        try:
            #load user
            pk = request.session['id']            

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Invite carers'),
                    'year': str(datetime.now().year),
                    'username': request.session["username"],
                }))
        except:
            if settings.DEBUG:
                print_exc()
            raise Http404

    def post(self, request):

        try:
            # load json data
            payload = json.loads(request.body)
            userId = int(payload['target']) # user id as carer

            #consumer= Consumers.objects.get(user_id = request.session['id'])
            s1, sender, consumer = getConsumerInfo(request)


            #carer   = Carers.objects.get(user_id = userId)
            s2, receiver, carer = getCarerInfo(request, userId)

            # insert record
            if ( CarersAssistConsumers.objects.filter(carer_id=carer.id).filter(consumer_id=consumer.id).count() == 0 ):
                nasRequest = CarersAssistConsumers(
                    carer_id=carer.id,
                    consumer_id=consumer.id,                
                    created_at=datetime.now()
                )
                nasRequest.save()

                # send notification to activate his/her account
                subject = "[P4ALL] Network of carers: invitation"
                to      = settings.RECEIVER_EMAIL if settings.DEBUG == True else [receiver.email]

                # Create agree/disagree links
                # path = '/assistance/invitations/reply'
                path = domainURL() + reverse('guided_assistance_reply_consumer_invitation')
                positiveLink = path + "?rec=" + str(receiver.email) + "&sen=" + str(sender.email) + "&val=" + str(nasRequest.id) + "&code=true"
                negativeLink = path + "?rec=" + str(receiver.email) + "&sen=" + str(sender.email) + "&val=" + str(nasRequest.id) + "&code=false"

                body = "<div>Dear " + receiver.name + " " + receiver.lastname + ",<br><br>"
                body += "The authorized AoD user, " + sender.name + " " + sender.lastname + ", wants to add you in his/her personal network of carers!<br>"
                body += "Do you want to grant permission on him/her?<br><br>"
                body += "If you agree, click here: <a href='" + positiveLink + " '>Accept</a><br><br>"
                body += "To decline it, click here: <a href='"+negativeLink+"'>Decline</a><br><br>"
                body += "Sincerely,<br>The AoD administration team</div>"
                
                # send email with HTML code
                sendEmail(to, subject, body, True)
                return JsonResponse({"state": True})
            else:
                return JsonResponse({"state": False, "message": "This request/invitation already has been submitted!"})
        except:
            print_exc()
            return JsonResponse({"state": False, "message": "Error"})

class NetworkAssistanceServicesCarerReply(View):

    def get(self, request):
        """ Carer reply on consumer invitation """
        try:
            carerEmail      = request.GET.get('rec')
            receiverEmail   = request.GET.get('sen')
            requestID       = request.GET.get('val')
            state           = True if request.GET.get('code') in ["true", True] else False
            
            if carerEmail and receiverEmail and requestID:
                carer     = Users.objects.get(email=carerEmail)
                consumer  = Users.objects.get(email=receiverEmail)
                
                CarersAssistConsumers.objects.filter(id=requestID, carer_id=Carers.objects.get(user_id=carer.id).id, consumer_id=Consumers.objects.get(user_id=consumer.id).id).\
                    update(response=True, state=state, updated_at=datetime.now())

                subject = "[P4ALL] Network of carer: reply"
                to      = settings.RECEIVER_EMAIL if settings.DEBUG == True else [receiver.email]
                
                # Advertise the carer's reply on consumer
                body = "<div>Dear " + consumer.name + " " + consumer.lastname + ",<br><br>"
                body += "The registered in AoD user, " + carer.name + " " + carer.lastname + ","
                if state == True:
                    body +=  " has accepted your invitation.<br>" +  carer.name + " is member of your personal network of carers.<br>"
                else: 
                    body +=  " has declined your invitation.<br>"
                body += "<br>Regards,<br>The AoD administration team</div>"

                # send email with HTML code
                sendEmail(to, subject, body, True)
                return redirect(reverse('guided_assistance_landing_page'))

        except ObjectDoesNotExist:
            print("Model does not exist")
            return Http404
        except MultipleObjectsReturned:
            print("Multiple instances founded")
            return Http404
        except:
            return Http404

@loginRequiredView
class NetworkAssistanceServicesFindUsers(View):
    def get(self, request):
        """
        Retrieve the consumer(s) having the entered email account
        """
        try:
            if request.is_ajax():
                uList = []
                # set email for lookup
                email = request.GET.get('email')
                loggedIn = request.session['id']

                users = Users.objects.filter(email=email)
                for i in users:
                    consumer = Consumers.objects.get(user_id=i.id)
                    relationship = CarersAssistConsumers.objects.filter(carer_id=loggedIn, consumer_id=consumer.id).count()
                    
                    # prevent requests to the logged in user, the user that are not consumer and  the existing relationships
                    if consumer.is_active and not relationship and i.id != loggedIn:
                        uList.append({"id": i.id, "name": i.name, "lastname": i.lastname, "email": i.email})

                return JsonResponse({"users": uList})
            else:
                raise Exception("No ajax request")
        except Exception as ex:
            return JsonResponse({"state" : -1})
        except:
            return JsonResponse({"state" : 0})   

@loginRequiredView
class NetworkAssistanceServices(View):

    def delete(self, request, pk):
        """ Remove an existing interest of carer """
        try:
            userID = request.session['id']

            if request.is_ajax():
                # delete object/instance
                nasRequest = CarersAssistConsumers.objects.get(pk=pk)
                nasRequest.delete()

                carerRequestData = []
                if request.session['is_carer']:
                    state, user, carer = getCarerInfo(request)
                    carerRecords = CarersAssistConsumers.objects.filter(carer_id=carer.id)
              
                    for obj in carerRecords:                    
                        consumer = Consumers.objects.get(pk=obj.consumer_id)
                        user = Users.objects.get(pk=consumer.user_id)
                        carerRequestData.append({
                            "id": str(obj.id),
                            "consumer_id": user.id, 
                            "name": user.name, 
                            "lastname": user.lastname, 
                            "response": obj.response,
                            "state": obj.state,
                            "created_at": obj.created_at,
                            "updated_at": obj.updated_at
                        });
                    return JsonResponse({"data": carerRequestData})

                consumerRequestData = []
                if request.session['is_consumer']:
                    state, user, consumer = getConsumerInfo(request)
                    carerRecords = CarersAssistConsumers.objects.filter(consumer_id=consumer.id)
              
                    for obj in carerRecords:
                        carer = Carers.objects.get(pk=obj.carer_id)
                        user = Users.objects.get(pk=carer.user_id)
                        consumerRequestData.append({
                            "id": str(obj.id),
                            "carer_id": user.id, 
                            "name": user.name, 
                            "lastname": user.lastname, 
                            "response": obj.response,
                            "state": obj.state,
                            "created_at": obj.created_at,
                            "updated_at": obj.updated_at
                        });
                    return JsonResponse({"data": consumerRequestData})

            else:
                raise Exception("No ajax")   
        except Exception as ex:
            return JsonResponse({"state" : -1})
        except:
            if settings.DEBUG:
                print_exc()
            return JsonResponse({"state" : 0})

@loginRequiredView
class NetworkAssistanceServicesConfiguration(View):
    
    def get(self, request, consumer):
        """ 
        Load the web page to send a new request to assist a consumer with disability
        """

        template = "app/carer-dashboard/configuration/index.html" 
        try:
            #load user
            pk = request.session['id']  
            consumerData  = Users.objects.get(id=consumer)

            catList = []
            cnt = 1
            for c in Categories.objects.filter(category_id = None):
                catList.append({"id": c.id, "title": c.title, "parent": -1, "order": cnt})
                for child in Categories.objects.filter(category_id = c.id):
                    catList.append({"id": child.id, "title": child.title, "parent": c.id})
                cnt += 1

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Network of assistance services'),
                    'categories': catList,
                    'services': Services.objects.all(),
                    'consumer': consumerData
                }))
        except:
            raise Http404

@loginRequiredView
class SearchNetworkAssistanceServices(View):
    def post(self, request):
        """ Loads the page related to the service listing and searching"""
        try :
            if request.is_ajax():
                assert isinstance(request, HttpRequest)
                pk = request.session['id']
                # load carer role id
                s1, user, carer = getCarerInfo(request, pk)

                # search options
                payload = json.loads(request.body)
                if settings.DEBUG == True:
                    print payload

                # load target consumer
                s2, targetUser, consumer = getConsumerInfo(request, payload['consumer_id'])

                # Categories
                mergeList, categories, subCategories = [], [], []
                if type(payload['categories']) is list and len(payload['categories']):
                    categories = payload['categories']
                    for i in payload['categories']:
                        for t in Categories.objects.filter(category_id=i):
                            subCategories.append(int(t.id))

                # merge lists
                mergeList = list(set(categories + subCategories))
                services = Services.objects.filter(categories__id__in=mergeList)
                uniqueServiceIDs = list(set(services.values_list('id', flat=True)))
                services = Services.objects.filter(pk__in=uniqueServiceIDs)

                # retrieve temp selected services
                tempSelectedServices = NasTemporarySetup.objects.filter(carer_id=carer.id, consumer_id=consumer.id)
                tempSelectedServicesList = [i.service_id for i in tempSelectedServices]

                # already purchased services (by individual user or carer)
                perUsagePolicy = ChargingPolicies.objects.filter(description__icontains="per usage")
                purchasedServicesList = [j.service_id for j in ConsumersToServices.objects.filter(consumer_id=consumer.id, is_completed=0).distinct()]

                # keep a list of unique IDs
                purchasedServicesList  = list(set(purchasedServicesList))

                # load services
                servicesList = []
                for service in services:
                    servicesList.append({
                        "id": service.id, 
                        "title":service.title, 
                        "description": service.description, 
                        "price":service.price, 
                        "unit":service.unit, 
                        "type": service.type,
                        "location_constraint": service.location_constraint,
                        "longitude": service.longitude,
                        "latitude": service.latitude,
                        "coverage": service.coverage,
                        "temp_selected": (service.id in tempSelectedServicesList),
                        "purchased": (service.id in purchasedServicesList),
                        "details_url": reverse('private_api:detailed_service', kwargs={'pk':service.id}),
                        "service_config_url": reverse('private_api:service_configuration', kwargs={'pk':service.id}),
                        "submit_service_url": reverse('guided_assistance_submit_services')
                    })
                
                return JsonResponse({"state": 1, "servicesList": servicesList})
            else:
                return JsonResponse({"state": -1})
        except: 
            if settings.DEBUG:
                print_exc()
            return JsonResponse({"state": -1})

@loginRequiredView
class NetworkAssistanceServicesQueue(View):

    def get(self, request):
        """
        Retrieve all the temporal selected services
        """
        try:
            if request.is_ajax():
                assert isinstance(request, HttpRequest)
                pk = request.session['id']
                s1, carerProfile, carer = getCarerInfo(request, pk)

                # target consumer
                s2, consProfile, consumer = getConsumerInfo(request, request.GET.get('consumer_id'))

                # Retrieve the list of temporal selected instances (NasTemporarySetup model)
                tempServices = NasTemporarySetup.objects.filter(carer_id=carer.id, consumer_id=consumer.id)
                tempServicesList = [i.service_id for i in tempServices]

                # Group the categories based on relationship parent-child
                response = []
                for grandparent in Categories.objects.filter(category_id=None):
                    categoriesDict  = dict()
                    categoriesIdList, servicesList    = [], []
                    categoriesDict["category"] = {"title": grandparent.title, "id": grandparent.id}

                    for parent in Categories.objects.filter(category_id=grandparent.id):
                        categoriesIdList.append(parent.id)
                        for child in Categories.objects.filter(category_id=parent.id):
                            categoriesIdList.append(child.id)
                  
                    # filter services and prepare response
                    for service in Services.objects.filter(pk__in=tempServicesList).filter(categories__id__in=set(list(categoriesIdList))).distinct():
                        servicesList.append({
                            "id": service.id, 
                            "title":service.title, 
                            "description": service.description, 
                            "price":service.price, 
                            "unit":service.unit, 
                            "type": service.type,
                            "location_constraint": service.location_constraint,
                            "longitude": service.longitude,
                            "latitude": service.latitude,
                            "details_url": reverse('private_api:detailed_service', kwargs={'pk':service.id}),
                            "service_config_url": reverse('private_api:service_configuration', kwargs={'pk':service.id}),
                            "submit_service_url": reverse('guided_assistance_submit_services')
                        })
                    categoriesDict['services'] = servicesList
                    response.append(categoriesDict)
               
                return JsonResponse({"state": 1, "servicesList": response})
            else:
                return JsonResponse({"state": -1})
        except:
            if settings.DEBUG:
                print_exc()
            return JsonResponse({"state": -1}, state=400)

    def post(self, request):
        """
        Simulate the push action in the queue
        """
        try :
            if request.is_ajax():
                assert isinstance(request, HttpRequest)
                pk = request.session['id']

                # search options
                payload = json.loads(request.body)
                if settings.DEBUG == True:
                    print payload

                # load carer profile
                s1, carerProfile, carer = getCarerInfo(request)
                # load consumer profile
                s2, consumerProfile, consumer = getConsumerInfo(request, payload['consumer_id'])

                # Insert instance in the NasTemporarySetup model
                tempAction = NasTemporarySetup(     
                    service_id=payload['service_id'],
                    carer_id=carer.id, 
                    consumer_id=consumer.id
                )
                tempAction.save()

                return JsonResponse({"state": 1})
            else:
                return JsonResponse({"state": -1})
        except Exception as ex: 
            print_exc()
            logger.exception(str(ex))
            return JsonResponse({"state": -1})

    def delete(self,request):
        """
        Simulate the pop action in the queue
        """
        try :
            if request.is_ajax():
                assert isinstance(request, HttpRequest)
                pk = request.session['id']

                # search options
                payload = json.loads(request.body)
                if settings.DEBUG == True:
                    print payload

                # load carer profile
                s1, carerProfile, carer = getCarerInfo(request)
                # load consumer profile
                s2, consumerProfile, consumer = getConsumerInfo(request, payload['consumer_id'])

                # Delete instance in the NasTemporarySetup model
                NasTemporarySetup.objects.filter(service_id=payload['service_id'], carer_id=carer.id, consumer_id=consumer.id).delete()

                return JsonResponse({"state": 1})
            else:
                return JsonResponse({"state": -1})
        except: 
            print_exc()
            return JsonResponse({"state": -1})

@loginRequiredView
class NetworkAssistanceServicesSubmit(View):
    def post(self, request):
        try :
            if request.is_ajax():
                assert isinstance(request, HttpRequest)
                pk = request.session['id']
                s1, carerProfile, carer = getCarerInfo(request)

                # load payload
                payload = json.loads(request.body)
                if settings.DEBUG == True:
                    print payload

                # target consumer
                s2, receiver, consumer = getConsumerInfo(request, payload['consumerID']) 

                # remove from queue
                tempService = NasTemporarySetup.objects.filter(service_id=payload['serviceID'], carer_id=carer.id, consumer_id=consumer.id).delete()
                
                # service info
                selService = Services.objects.get(pk=payload['serviceID'])

                #insert into nas table
                nas = ConsumersToServices(     
                    service_id=payload['serviceID'],
                    purchased_date=datetime.now(),
                    consumer_id=consumer.id,
                    cost=selService.price,
                    nas_aware=True
                )
                nas.save()
                curSrvId = nas.id

                # send email notification to consumer
                to = settings.RECEIVER_EMAIL if settings.DEBUG == True else  [receiver.email]

                subject     = "[P4ALL] Network of assistance services: purchase service"
                body        = "<div>Dear <strong>" + receiver.name + " " + receiver.lastname + "</strong>,<br><br>"
                body        += "The authorized AoD user, " + carerProfile.name + " " + carerProfile.lastname + ", just purchased the service <em>"+selService.title+"</em> for you a few minutes ago!<br>"
                body        += "<br>Sincerely,<br>The AoD administration team</div>"
                sendEmail(to, subject, body, True)

                return JsonResponse({"state": 1, "id": curSrvId, "consumerId": payload['consumerID']})
            else:
                return JsonResponse({"state": -1})
        except Exception as e: 
            print e
            print_exc()
            return JsonResponse({"state": -1})

@loginRequiredView
class SearchKwdNetworkAssistanceServices(View):

    def post(self, request):
        try:
            if request.is_ajax():
                assert isinstance(request, HttpRequest)
                pk = request.session['id']

                # load payload
                payload = json.loads(request.body)
                if settings.DEBUG == True:
                    print payload

                consumer = Consumers.objects.get(user_id = payload['consumerID'])

                if 'keywords' in payload and 'consumerID' in payload:
                    keyword = payload['keywords']

                    # already purchased services (by individual user)
                    # purchasedServicesList = ConsumersToServices.objects.filter(consumer_id=consumer.id, is_completed=0).distinct().values_list('service_id', flat=True)
                    purchasedServicesList = ConsumersToServices.objects.filter(consumer_id=consumer.id, is_completed=0).distinct().values_list('service_id', flat=True)
                    # search for keywords in service title/description and service keywords
                    servicesKwdList = [k.service_id for k in ServiceKeywords.objects.filter(title__icontains=keyword).distinct()]

                    # retrieve services
                    services = Services.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(pk__in=servicesKwdList))
                    if len(purchasedServicesList) > 0:
                        services = services.exclude(pk__in=purchasedServicesList)
                    services = services.distinct()

                    servicesList = []
                    for service in services:
                        servicesList.append({
                            "id": service.id, 
                            "title":service.title, 
                            "description": service.description, 
                            "price":service.price, 
                            "unit":service.unit, 
                            "type": service.type,
                            "location_constraint": service.location_constraint,
                            "longitude": service.longitude,
                            "latitude": service.latitude,
                            "coverage": service.coverage,
                            "details_url": reverse('private_api:detailed_service', kwargs={'pk':service.id}),
                            "service_config_url": reverse('private_api:service_configuration', kwargs={'pk':service.id}),
                            "submit_service_url": reverse('guided_assistance_submit_services')
                        })
                
                    return JsonResponse({"state": 1, "data": servicesList})
            
                return JsonResponse({"data": []})
        except Exception as ex:
            logger.exception(str(ex))    
            if settings.DEBUG:    
                print_exc()
            return Http404

@loginRequiredView
class PreviewNetworkAssistanceServices(View):
    def get(self, request, user):
        try:
            assert isinstance(request, HttpRequest)
            pk = request.session['id']
            carer = Carers.objects.get(user_id = pk)

            template = "app/carer-dashboard/preview/index.html"
            
            consumer = Consumers.objects.get(user_id=user)
            consumerProfile = Users.objects.get(pk=user)
            
            selectedList = [s.service_id for s in NasTemporarySetup.objects.filter(carer_id=carer.id, consumer_id=consumer.id)]
            selectedServicesList = Services.objects.filter(pk__in=selectedList)
                
            purchasedList = [p.service_id for p in ConsumersToServices.objects.filter(consumer_id=consumer.id)]
            purchasedServicesList = Services.objects.filter(pk__in=purchasedList)
                
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Network of assistance services preview'),
                    'year': str(datetime.now().year),
                    'selectedServices': selectedServicesList,
                    'purchasedServices': purchasedServicesList,
                    'consumer': {'id': consumer.id, 'info': consumerProfile.name + " " + consumerProfile.lastname}
                }))
        except Exception as ex:
            print_exc()        
            print str(ex)

@loginRequiredView
class ServiceConfigurationView(View):

    def get(self, request, pk):
        try:
            if request.is_ajax():
                assert isinstance(request, HttpRequest)

                config  = ServiceConfiguration.objects.filter(service_id=pk)
                data    = serializers.serialize("json", config)
                return JsonResponse({"data": json.loads(data)})

            return JsonResponse({"state": -1, "data": []})
        except Exception as ex:
            return JsonResponse({"state": -1, "data": []})

@loginRequiredView
class ServiceInstance(View):

    def get(self, request, pk):
        try:
            if request.is_ajax():
                assert isinstance(request, HttpRequest)

                service  = Services.objects.get(pk=pk)

                languages, langList = None, ''
                import pycountry
                languages = ServiceLanguages.objects.filter(service_id=pk)
                for l in pycountry.languages:
                    for i in languages:
                        if i.alias == l.terminology:
                            langList += l.name + ", "

                # load template
                return JsonResponse(
                    {
                        'title': service.title, 
                        'description': service.description,
                        'type': 'Human-based' if service.type=='H' else 'Machine-based',
                        'charging_policy': ChargingPolicies.objects.get(id=service.charging_policy_id).name,
                        'price': '-' if service.price == 0 else service.price,
                        'unit': service.unit,
                        'requirements': service.requirements,
                        'installation_guide': service.installation_guide,
                        'usage_guidelines': service.usage_guidelines,
                        'constraints': service.constraints,
                        'languages': langList,
                        'longitude': service.longitude,
                        'latitude': service.latitude
                    }
                )

            return JsonResponse({"state": -1, "data": []})
        except Exception as ex:
            import traceback
            traceback.print_exc()
            return JsonResponse({"state": -1, "data": []})


#==============================
#   Handle template errors
#==============================
def forgetPassword(request):
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/errors/404.html',
        context_instance = RequestContext(request,
        {
            'title': _('Page no Found'),
            'year':datetime.now().year,
        }))

def not_found(request):
    """ Handle the 404 http status """
    
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/errors/404.html',
        context_instance = RequestContext(request,
        {
            'title': _('Page not Found'),
            'year':datetime.now().year,
        }))

def method_not_allowed(request):
    """ Handle the 405 http status """

    assert isinstance(request, HttpRequest)
    return render(request,
        'app/errors/404.html',
        context_instance = RequestContext(request,
        {
            'title': _('HTTP method not allowed'),
            'year':datetime.now().year,
        }))

def server_error(request):
    """ Handle the 500 http status """

    assert isinstance(request, HttpRequest)
    return render(request,
        'app/errors/500.html',
        context_instance = RequestContext(request,
        {
            'title': _('Internal server error'),
            'year':datetime.now().year,
        }))


#==============================
#   Calendar
#==============================
@loginRequiredView
class CalendarView(View):

    def get(self, request, username):
        """
        Retrieve the list of events
        """
        try:
            template = "app/prosumers/calendar/index.html" 

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _(' My calendar'),
                    'year': str(datetime.now().year),
                })
            )
        except:
            if settings.DEBUG:
                print_exc()
            raise Http404


#==============================
#   Cookie Policy
#==============================
class CookiePolicyView(View):
    """Manage AoD cookie policy"""

    def get(self, request):
        """Load context of AoD cookie policy"""
        try:
            template = "app/cookiePolicy.html" 
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Cookies Policy'),
                    'year': str(datetime.now().year),
                    'username': request.session["username"] if "username" in request.session else None,
                    'policy': CookiePolicy.objects.get(active=True),
                }))
        except:
            print_exc()
            raise Http404


#==============================
#   Service rating
#==============================
@loginRequiredView
class ServiceRatingView(View):

    def post(self, request, pk=None):
        """Insert the service review of a consumer"""

        try:
            if request.is_ajax():
                # load json data
                payload = json.loads(request.body)
                consumer = Consumers.objects.get(user_id=request.session['id'])

                if ConsumerServiceEvaluation.objects.filter(consumer_id=consumer.id, service_id=pk).count():
                    raise MultipleObjectsReturned(_("Review has already submitted for this service"))

                # insert ConsumerServiceEvaluation objects for each metric
                sum_eval, count_eval = 0.0, 0.0
                for key in payload:
                    if key.startswith("evaluation_metric_"):
                        metric_id = key.split("evaluation_metric_")[-1]
                        eval_metric = EvaluationMetric.objects.get(pk=metric_id)

                        if float(payload[key]) > float(eval_metric.max_score) or float(payload[key]) < float(eval_metric.min_score):
                            metric_name = eval_metric.name_en.encode('utf-8')
                            raise Exception(_("The value of the metric {} is out of range. Enter a value in range [{},{}]").format(metric_name, eval_metric.min_score, eval_metric.max_score))

                        consumer_metric_eval_service = ConsumerServiceEvaluation(
                            consumer_id=consumer.id,
                            service_id=pk,
                            evaluation_metric_id=metric_id,
                            score=payload[key]
                        )
                        consumer_metric_eval_service.save()

                        sum_eval += float(payload[key]) * eval_metric.weight
                        count_eval += eval_metric.weight

                # Insert consumer rating and comments
                consumer_avg_score = float(sum_eval/count_eval)
                consumer_to_service = ConsumersToServices.objects.filter(service_id=pk, consumer_id=consumer.id).order_by('-id').first()
                ConsumersToServices.objects.filter(pk=consumer_to_service.id).update(
                    rating=consumer_avg_score,
                    advantages=payload.get('advantages', None),
                    disadvantages=payload.get('disadvantages', None),
                    rating_rationale=payload.get('rating_rationale', None),
                    review_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )                

                # update the service review details 
                service = Services.objects.get(pk=pk)
                if service.id > 0:
                    updated_score = ((service.review_score * service.reviews_count) + consumer_avg_score)/(service.reviews_count+1)
                    Services.objects.filter(pk=pk).update(review_score=updated_score, reviews_count=(service.reviews_count+1))
                else:
                    # roll back
                    ConsumerServiceEvaluation.objects.filter(service_id=pk).delete()
                    ConsumersToServices.objects.filter(service_id=pk).delete()
                    raise Exception(_("Error in service review has detected"))    

                return JsonResponse(data={"message": _("Your review has been submitted successfully!")}, status=200)

            return HttpResponseRedirect(reverse("service_view_page", kwargs={'pk':pk}))

        except MultipleObjectsReturned as mx:
            logger.exception(str(mx))
            return JsonResponse(data={"error":str(mx)}, status=409)
        except Exception as ex:
            logger.exception(str(ex))
            return JsonResponse(data={"error":str(ex)}, status=400)


@loginRequiredView
class ServiceUsageView(View):

    def post(self, request, pk=None):
        """Associate a consumer with a service to highlight that user uses it.

        Set the state of the resource as True. 
        """
        try:
            user_id = request.session['id']
            consumer = Consumers.objects.get(user_id=user_id)

            consumer_use_service = ConsumersToServices.objects.create(
                consumer=consumer,
                service_id=pk,
                purchased_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                is_completed=True,
                access_resource=True
            )

            return HttpResponseRedirect(reverse("service_view_page", kwargs={'pk': pk}))
        except Exception as ex:
            logger.exception(str(ex))
            return HttpResponseRedirect(reverse("service_view_page", kwargs={'pk': pk}))


#==============================
#   Try different
#==============================            
class UserSearchPreferences(View):

    def post(self, request):
        """Keep the last preferences of  authenticated user during his search"""

        try:
            if request.is_ajax():
                if 'id' in request.session.keys():
                    user_id = request.session['id']
                    params = request.body

                    tracks = TrackUserSearch.objects.filter(user_id=user_id)
                    if tracks.count() > 0:
                        tracks.update(preferences=params)
                    else:
                        TrackUserSearch.objects.create(user_id=user_id, preferences=params)
                    return JsonResponse({}, status=200)

                else:
                    raise Exception("Action is not allowed")
            else:
                raise Http404

        except Exception as ex:
            logger.exception(str(ex))
            return JsonResponse({}, status=400)
        except:
            return JsonResponse({}, status=500)


@loginRequiredView
class ServiceDownloadResourceView(View):
    """Track the download of the service resource of a consumer to disable the pop up window"""

    def post(self, request, pk):
        try:
            if request.is_ajax():
                if 'id' in request.session.keys():
                    user_id = request.session['id']
                    consumer = Consumers.objects.get(user_id=user_id)
                    service = Services.objects.get(pk=pk)
                    consumer_to_services = ConsumersToServices.objects.filter(consumer=consumer, service=service, access_resource=True)

                    if service.charging_policy.id == 2:
                        now = datetime.now()
                        consumer_to_services = consumer_to_services.filter(purchased_date__gt=now, end_date__lt=now)
                    else: 
                        consumer_to_services = consumer_to_services.filter(end_date__isnull=True)

                    resource_downloads = 0
                    if consumer_to_services.count() > 0:
                        resource_downloads = consumer_to_services.first().download
                        resource_downloads += 1
                        consumer_to_services.update(download=resource_downloads)
                        return JsonResponse(data={}, status=200)
                    return JsonResponse(data={}, status=400)

                return JsonResponse(data={}, status=401)

            return redirect(reverse('service_view_page', kwargs={'pk', pk}))
        except Exception as ex:
            logger.exception(str(ex))
            return redirect(reverse('service_view_page', kwargs={'pk', pk}))
        