"""
Definition of views.
"""

from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import Http404, HttpRequest, HttpResponseServerError, JsonResponse, HttpResponse, HttpResponseRedirect

from django.template import RequestContext
from django.template.response import TemplateResponse
from django.template.loader import render_to_string

from django.views.generic import View, CreateView, UpdateView, DeleteView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe

from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.contrib import messages

from django.db.models import Avg, Sum, Q
from django.db import IntegrityError

from django.utils import timezone

from app.models import *        # import models
from app.decorators import *    # import custom models

from functools import wraps
from datetime import datetime   # date/time module
import pytz
import json                     # json lib
import urllib

from django.conf import settings

from traceback import print_exc



#################################
##      Visitor home page
#################################
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    try:
        # most popular service
        popularity, popularService = [], []
        for i in Services.objects.all():
            popularity.append({"id":i.id, "count": ConsumersToServices.objects.filter(service_id=i.id).count()})
        sortedlist = sorted(popularity, key=lambda k: k['count'], reverse=True)
        service = Services.objects.get(id=sortedlist[0]["id"])
        popularService.append({"id": service.id, "title":service.title, "description": service.description, 
            "price":service.price, "unit":service.unit, "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
            "rating": ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0], 
            "reviews": ConsumersToServices.objects.filter(service_id=service.id).count(), "type": service.type
            }
        )

        # most recently service
        latestService = []
        service = Services.objects.all().order_by("-created_date")[0]
        latestService.append({"id": service.id, "title":service.title, "description": service.description, 
                "price":service.price, "unit":service.unit, "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                "rating": ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0], "reviews": ConsumersToServices.objects.filter(service_id=service.id).count(), "type": service.type})

        return render(request,
            'app/visitors/home.html',
            context_instance = RequestContext(request,
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'popularService': popularService[0],
                'latestService': latestService[0],
            }))
    except:
        return render(request,
            'app/visitors/home.html',
            context_instance = RequestContext(request,
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'popularService': None,
                'latestService': None
            }))

#################################
##      Registration 
#################################
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
                    'title':'Registration page',
                    'year':datetime.now().year,
                    'title': "AoD | Registration",
                    'experience': ItExperience.objects.all().order_by('id'),
                    'CountriesList': result,
                    'categories': Categories.objects.all().order_by('id'),
                    'literal': literal
                }))
        except:
            # response: 404 not found
            pass

    def post(self, request):
        """ Submit and store the information of new user """

        # If the <request> is a HttpRequest object continue.  Else raise an
        # Exception
        assert isinstance(request, HttpRequest)

        # Registration process
        try:
            instance = json.loads(request.body)

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
                        provider = Providers(user=Users.objects.get(pk=_pk), is_active=True, company="N/A")
                        provider.save()
                    if i in ["Consumer", "consumer", "CONSUMER"]:
                        consumer = Consumers(user=Users.objects.get(pk=_pk), crowd_fund_notification=instance['crowd_notification'], crowd_fund_participation=instance['crowd_participation'], is_active=True)
                        consumer.save()
                    if i in ["Carer", "carer", "CARER"]:
                        carer = Carers(user=Users.objects.get(pk=_pk), is_active=True)
                        carer.save()
                else:
                    # cases
                    if i in ["Provider", "provider", "PROVIDER"]:
                        provider = Providers(user=Users.objects.get(pk=_pk), is_active=False, company="N/A")
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

            to = [user.email]

            domain =  request.scheme  + "://" +  request.META['HTTP_HOST'] 

            # create a hash for activation link
            hash = hashPassword(user.email)

            # send notification to activate his/her account
            from django.core.mail import send_mail
            subject = "AoD Registration"
            body = "Dear "+str(user.name) +" " + str(user.lastname)+",\n\n"
            body += "Your registration was successfully completed in the AoDemand marketplace.\n"
            body += "The required username is: " + user.username+".\n"
            body += "Please follow the below link to activate your account:\n\n"
            body += domain+ "/account/activation?p="+ user.email +"&q="+ hash + "\n\n"
            body += "We don't check this mailbox, so please don't reply to this message.\n\n"
            body += "Sincerely,\nThe AoD administrator team"
            # send email
            send_mail(subject, body, 'no-reply@p4all.com', to, fail_silently=False)

            # server response in success
            return JsonResponse({"state": True, "redirect": domain+"/account/signup-success/"})
            
        except:  
            # server response in failure
            return JsonResponse({"state": False})
  
def registrationSuccess(request,):
    """ Whether registration was successfully completed, redirect user """
    return render(request,
        'app/visitors/registration_success.html',
        context_instance = RequestContext(request,
        {
            'year':datetime.now().year,
            'username': "user",
            'title': "AoD Registration"
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


#################################
##      Account activation 
#################################
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
                    'title':'About',
                    'message':"<center><span class='label label-primary' role='contentinfo'><i class='fa fa-info-circle fa-fw'></i> Your account was activated.</span></center>",
                    'year': "" + datetime.now().year,
                }))
        raise Exception("Activation was expired.") 
       
    except Exception as e:
        # handle any exception
        return render(request,
            'app/visitors/login.html',
            context_instance = RequestContext(request,
            {
                'title':'About',
                'message': "<center>"+str(e.args[0])+"</center>",
                'year': datetime.now().year,
            }))

    except:
        raise Exception("Activation was expired.")

#################################
##  Forgot password
#################################
class ForgotPasswordView(View):
    def get(self, request):
        """ Enter the email account """
        try:
            assert isinstance(request, HttpRequest)
            template = 'app/visitors/forgot-password.html'
            
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Forgot password',
                    'year':datetime.now().year,
                }))                
        except:
            raise Http404

#################################
##      Log in 
#################################
def login(request):
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/visitors/login.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':None,
            'year':datetime.now().year,
        }))

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
        
        # move to his dashboard
        return redirect('/index')

    except Exception as e:
        # preview the following message on user
        details = '<center><span class="label label-danger" role="contentinfo"><i class="fa fa-exclamation-circle fa-lg fa-fw"></i> Wrong combination of your credentials and your role. Try again.</span></center><br>'        
        
        return render(request,
            'app/visitors/login.html',
            context_instance = RequestContext(request,
            {
                'message': details,
                'year':datetime.now().year,
            }))
        
    except:
        raise Exception("server error")  


#################################
##      Handle Profile 
#################################
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
    template = 'app/consumers/profile/personal-info.html'

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
    template = 'app/consumers/profile/contact-info.html'

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
                    'images': {'cover': {'exist': False, 'path': ''}, 'profile': {'exist': True, 'path': '../../../static/app/images/home/users/128.jpg'}}
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
    template = 'app/consumers/profile/platform-info.html'
    
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
                    'images': {'cover': {'exist': False, 'path': ''}, 'profile': {'exist': True, 'path': '../../../static/app/images/home/users/128.jpg'}}
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



#################################
##  User IT experience (R)
#################################
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

#################################
##  Countries (R)
#################################
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


#################################
## Users: Consumer/Provider/Carer
#################################
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
                    'title': 'Bad request!',
                }))

        template = 'app/consumers/profile.html'
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
                'links': navbarLinks(request),
                'breadcrumb': breadcrumbLinks(request),
                'username': username,
                'roles': roles,
                'media_url': "/profile/media/" + str(pk),
                'error': False,
                'cover': settings.MEDIA_URL + "app/users/covers/" + str(customer.cover),
                'logo': settings.MEDIA_URL + "app/users/logos/" + str(customer.logo)
            }))
    except:
        raise Http404

def navbarLinks(request):
    """
    Return the links of navigation-bar in case of registered user
    """
    links = dict()
    links['index']          = "/index"
    links['profile']        = "/profile/"+str(request.session['username'])
    links['collection']     = "/provider"
    links['stats']          = "/my-statistics/preview"
    links['setup_network']  = "#"
    links['help']           = "/support"
    links['cart']           = "/cart/preview"
    links['cart_items']     = 0
    if 'cart' in request.session:
        links['cart_items'] = len(request.session['cart'])

    links['notifications']  = "#"
    links['social_network']  = "http://160.40.51.143:40000/aodsocial/app/#/home?email=maher@email123.com&info=demo123!"

    # Network of assistance services
    nasExistance = Components.objects.get(name='network_of_assistance_services')
    links['is_nas_active']  = nasExistance.is_enabled
    links['nas_requests']   = "/assistance/requests"
    links['nas_configuration']    = "/assistance/configuration"
    return links

def breadcrumbLinks(request):
    """
    Return the breadcrumb' links in case of registered user
    """
    links = dict()
    links['home']           = "/index"
    links['collection']     = "/offerings"
    links['services']       = "/offerings/services"
    links['nas_requests']   = "/assistance/requests"
    links['create_nas_request']= "/assistance/requests/create-new"
    return links

def getTimeZone():
    return settings.TIME_ZONE

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


#################################
## Services - providers
#################################
@loginRequiredView
class ServiceSearch(View):
    def get(self, request):
        """ Loads the page related to the service listing and searching"""
        try :
            assert isinstance(request, HttpRequest)
            template = 'app/consumers/dashboard.html'    
            pk = request.session['id']

            # view
            view = 'm'
            if request.GET.get('view') != None:
                view = request.GET.get('view')

            # Sort services by user choice
            sortby = "title"
            if request.GET.get('sortby') != None:
                sortby = sortByMap(request.GET.get('sortby'))  

            # Filter services per page
            limit = 30
            if request.GET.get('limit') != None:
                limit = sortByMap(request.GET.get('limit')) 

            # Filter services by charging model 
            chModel = [1,2,3,4,5]
            if request.GET.get('model') not in [0, None] and int(request.GET.get('model')):
                chModel = []
                chModel.append(request.GET.get('model')) 
 
            # customer-user info        
            user = Users.objects.get(pk=pk)

            # providers
            providers = []
            for i in Providers.objects.all():
                if i.is_active:
                    u =  Users.objects.get(id=i.user_id)
                    providers.append({"id": i.id, "name": u.name + " "+u.lastname, "servNo": Services.objects.filter(owner_id=i.id).count()})

            # categories
            categories = []
            #categories.append({"id":all, "title": "All", "servNo": Services.objects.count() })
            for category in Categories.objects.all().order_by("title"):
                categories.append({"id":category.id, "title": category.title, "servNo": Services.objects.filter(categories__id=category.id).count() })   

            # charging models
            chModels = []
            for model in ChargingPolicies.objects.all().order_by("id"):
                chModels.append({"id": model.id, "name":model.name, "servNo": Services.objects.filter(charging_policy_id=model.id).count() })

            # services
            servicesInfo = []

            if request.GET.get('type') not in [None, "A"]:
                for service in Services.objects.filter(type=request.GET.get('type')).filter(charging_policy_id__in=chModel).order_by(sortby)[:limit]:
                    servicesInfo.append({"id": service.id, "title":service.title, "description": service.description, "cover": service.cover,
                        "price":service.price, "unit":service.unit, "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                        "rating": ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0], 
                        "reviews": ConsumersToServices.objects.filter(service_id=service.id).count(), "type": service.type,
                        "logo": Users.objects.get(pk=service.owner_id).logo.name, "alias":  urllib.quote_plus(service.title),
                        "image": service.image
                    })
            else:
                for service in Services.objects.filter(charging_policy_id__in=chModel).order_by(sortby)[:limit]:
                    servicesInfo.append({"id": service.id, "title":service.title, "description": service.description, "cover": service.cover,
                        "price":service.price, "unit":service.unit, "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                        "rating": ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0], 
                        "reviews": ConsumersToServices.objects.filter(service_id=service.id).count(), "type": service.type,
                        "logo": Users.objects.get(pk=service.owner_id).logo.name, "alias":  urllib.quote_plus(service.title),
                        "image": service.image
                    })


            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'userID': request.session['id'],
                    'username': request.session['username'],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                    'providers': providers,
                    'categories': categories,
                    'servicesTypes': {'all': Services.objects.all().count(), 'human': Services.objects.filter(type='H').count(), 'machine': Services.objects.filter(type='M').count()},
                    'chargingModels': chModels,
                    'services': servicesInfo,
                    'sortby': request.GET.get('sortby'),
                    'view': view
                }))
        except: 
            redirect('/logout')

@loginRequiredView
class ServiceSearchResults(View):
    def post(self, request):
        """ Return the result of search """
        template = 'app/consumers/services/services.html'

        try :
            if request.is_ajax():
                assert isinstance(request, HttpRequest)
                pk = request.session['id']
                # customer-user info        
                user = Users.objects.get(pk=pk)

                # search options
                payload = json.loads(request.body)
                print payload
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
                                        servicesInfo.append({"id": service.id, "title":service.title, "description": service.description, "cover": service.cover,
                                            "price":service.price, "unit":service.unit, "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                                            "rating": rating, "reviews": reviews, "type": service.type,
                                            "logo": Users.objects.get(pk=service.owner_id).logo.name, "alias":  urllib.quote_plus(service.title)
                                        })
                                else:
                                    servicesInfo.append({"id": service.id, "title":service.title, "description": service.description, "cover": service.cover,
                                        "price":service.price, "unit":service.unit, "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                                        "rating": rating, "reviews": reviews, "type": service.type,
                                        "logo": Users.objects.get(pk=service.owner_id).logo.name, "alias":  urllib.quote_plus(service.title)
                                    })
                                    
                else:
                    for service in s.order_by(sortby)[:limit]:
                        # check QoS
                        rating = ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0]
                        reviews = ConsumersToServices.objects.filter(service_id=service.id).count()
                                
                        if minQoS != None and maxQoS != None:
                            if int(reviews) > 0 and float(minQoS) <= float(rating) <= float(maxQoS):
                                servicesInfo.append({"id": service.id, "title":service.title, "description": service.description, "cover": service.cover,
                                    "price":service.price, "unit":service.unit, "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                                    "rating": rating, "reviews": reviews, "type": service.type,
                                    "logo": Users.objects.get(pk=service.owner_id).logo.name, "alias":  urllib.quote_plus(service.title)
                                })
                        else:
                            servicesInfo.append({"id": service.id, "title":service.title, "description": service.description, "cover": service.cover,
                                "price":service.price, "unit":service.unit, "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                                "rating": rating, "reviews": reviews, "type": service.type,
                                "logo": Users.objects.get(pk=service.owner_id).logo.name, "alias":  urllib.quote_plus(service.title)
                            })

                response_dic = {
                        'services': servicesInfo,
                        'sortby': sortby,
                        'view': view
                    }

                return render(request, template, response_dic)
            else:
                return redirect("/index")

        except AttributeError as at:
            print "400"
        
        except:
            print "500"
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


@loginRequiredView
class ServicesIndex(View):
    def get(self, request):
        """
        Get the list of offering services per provider
        """

        try:
            template = 'app/consumers/services/list/index.html'

            user = Users.objects.get(pk=request.session['id'])
            _owner = Providers.objects.get(user_id=user.id)
            servicesInfo = []
            for service in Services.objects.filter(owner=_owner.id):
                servicesInfo.append({"id": service.id, "alias": urllib.quote_plus(service.title), 
                    "title":service.title, "description": service.description, 
                    "price":service.price, "unit":service.unit, "type": service.type,
                    "access": service.availability, "available": service.is_available,
                    "charge_model": ChargingPolicies.objects.get(id=service.charging_policy_id),
                    "rating": ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0], 
                    "reviews": ConsumersToServices.objects.filter(service_id=service.id).count(), 
                    "created_date": service.created_date, "modified_date": service.modified_date
                })

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'username': request.session['username'],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                    'servicesLink': '/provider/services',
                    'servicesTypes': {'all': Services.objects.all().count(), 'human': Services.objects.filter(type='H').count(), 'machine': Services.objects.filter(type='M').count()},
                    'services': servicesInfo,
                }))

        except:
            pass

@loginRequiredView
class ServiceCreate(View):
    def get(self, request):
        try:
            template = 'app/consumers/services/registration/index.html'
            pk=request.session['id']
            user = Users.objects.get(pk=pk)

            # Available types
            types = []
            types.append({'id': 'H', "description": 'Human Based'})
            types.append({'id': "M", "description": "Machine Based"})

            # cover images
            covers = getDefaultCoverList()

            # languages
            import pycountry
     
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                    'username': request.session['username'],
                    'types': types,
                    'categories': Categories.objects.all().order_by('id'),
                    'covers': covers,
                    'charging_models': ChargingPolicies.objects.all(),
                    'currencies': pycountry.currencies,
                    'users': Users.objects.exclude(pk=pk).order_by('email'),
                    'languages': pycountry.languages
                }))
    
        except:
           return redirect('/')

    def post(self, request):
        """
        Create a new service of a provider
        """

        try:
            # Valid or exception
            assert isinstance(request, HttpRequest)
            pk = request.session['id']

            # Parse the client payload
            payload = json.loads(request.body)
            if not payload:
                raise Exception("JSON payload error")

            if settings.DEBUG:
                print payload

            # Create a new service
            dt = datetime.today()
            
            service = Services(title=payload['srv_title'], 
                description=payload['srv_description'],
                # logo
                version=payload['srv_version'],
                license=payload['srv_license'],
                cover=payload["srv_cover_image"],
                type=payload["srv_type"],
                # "srv_keyword_list"
                charging_policy=ChargingPolicies.objects.get(pk=payload["srv_charging_model"]),
                owner=Providers.objects.get(user_id=pk),
                price=payload["srv_price"],
                unit=payload["srv_currency"],
                requirements=payload["srv_requirements"],
                installation_guide=payload["srv_installation"],
                # package
                link=payload["srv_link"],
                usage_guidelines=payload["srv_usage"],
                availability=payload["availability"],
                # target group of users or none
                constraints=payload["srv_constraints"],
                language_constraint=payload["srv_language_constraint"],
                location_constraint=payload["srv_geolocation"],
                latitude=payload["srv_latitude"],
                longitude=payload["srv_longitude"],
                skype=payload["skype_id"],
                coverage=payload["srv_coverage"],
                is_available=payload["srv_terms"],
                modified_date=datetime(1970,1,1,0,0,0, tzinfo=pytz.timezone(getTimeZone())),
                created_date=dt
            )
             
            # store a new service
            try:
                service.save()
            except IntegrityError as i:
                # http 409 confict: duplicate unique, invalid foreign key
                raise Exception(i.args[0], i.args[1])
            
            _service = service.id

            # Associate service with desired categories
            categories = payload['srv_category']
            if type(categories) == list:
                for i, v in enumerate(categories):
                    service.categories.add(v)
            elif type(categories) in [str, int]:
                service.categories.add(v)
            else:
                raise Exception("Categories input neither list nor string/integer")

            # keywords
            keywords = payload['srv_keywords']
            if type(keywords) == list:
                for i in keywords:
                    if i is not None:
                        k = ServiceKeywords(service=Services.objects.get(pk=_service), title=i)
                        k.save()
            elif type(keywords) is str:
                k = ServiceKeywords(service=Services.objects.get(pk=_service), title=i)
                k.save()

            # languages
            languages = payload['srv_language']
            if type(languages) == list:
                for i in languages:
                    if i is not None:
                        l = ServiceLanguages(service=Services.objects.get(pk=_service), alias=i)
                        l.save()
            elif type(languages) is str and not None:
                l = ServiceLanguages(service=Services.objects.get(pk=_service), alias=i)
                l.save()

            links = breadcrumbLinks(request)
            return JsonResponse({"state": True, "link": links["collection"], "id": _service})
        except Exception as e:
            return JsonResponse({"state": False, "reason":e.args})            
        except:
             return JsonResponse({"state": "False2"})

@loginRequiredView
class ServiceView(View):
    def get(self, request, alias=None):
        """ 
        Preview of the service for provider 
        """

        try:
            template = 'app/consumers/services/item/preview/index.html'
            
            # service and provider info
            user = Users.objects.get(pk=request.session['id'])
            provider = Providers.objects.get(user_id=user.id)
            title = urllib.unquote_plus(alias)

            # service instance
            service = Services.objects.get(title=str(title))
            keywords = ServiceKeywords.objects.filter(service=service.id).all()
            languages = []
            import pycountry
            for lang in ServiceLanguages.objects.filter(service=service.id).all():
                for i in pycountry.languages:
                    if lang.alias == i.terminology:
                        languages.append(i.name)

            reviews = []
            for i in ConsumersToServices.objects.filter(service_id=service.id):
                u = Users.objects.get(pk=i.consumer_id)
                c = ChargingPolicies.objects.get(pk=Services.objects.get(pk=service.id).charging_policy_id)
                reviews.append({"user": u.name +" " + u.lastname, "rating": i.rating, 'comment': i.rating_rationale, 
                    'purchased_date': i.purchased_date, 'price': i.cost, "unit": service.unit})

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'username': request.session['username'],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                    'servicesLink': '/provider/services',
                    'service': service,
                    'keywords': keywords,
                    'categories': service.categories.all(),
                    'languages': languages,
                    'reviews': reviews,
                }))

        except:
            pass

    def put(self, request, alias=None):
        """ 
        Update an existing service data
        """

        try:
            # check request type
            assert isinstance(request, HttpRequest)
            # check if alias exist
            if alias == None:
                raise Exception("Invalid alias")
            _title = urllib.unquote_plus(alias)

            payload = json.loads(request.body)
            if not payload:
                raise Exception("JSON payload error")

            # Create a new service
            Services.objects.filter(title=_title).update(
                title=payload['srv_title'], 
                description=payload['srv_description'],
                # logo
                version=payload['srv_version'],
                license=payload['srv_license'],
                # cover=payload["srv_cover_image"],
                type=payload["srv_type"],
                # "srv_keyword_list"
                charging_policy=ChargingPolicies.objects.get(pk=payload["srv_charging_model"]),
                price=payload["srv_price"],
                unit=payload["srv_currency"],
                requirements=payload["srv_requirements"],
                installation_guide=payload["srv_installation"],
                # package
                link=payload["srv_link"],
                usage_guidelines=payload["srv_usage"],
                availability=payload["availability"],
                # target group of users or none
                constraints=payload["srv_constraints"],
                language_constraint=payload["srv_language_constraint"],
                location_constraint=payload["srv_geolocation"],
                latitude=payload["srv_latitude"],
                longitude=payload["srv_longitude"],
                is_available=payload["srv_terms"],
                modified_date=datetime.today()
            )

            # service instance
            service = Services.objects.get(title=payload['srv_title'])
            _service = service.id

            print "OK 1"

            # Delete existing categories
            for i in service.categories.all():
                service.categories.remove(i)
            # Create relationships
            categories = payload['srv_category']
            if type(categories) == list:
                for i, v in enumerate(categories):
                    service.categories.add(v)
            elif type(categories) in [str, int]:
                service.categories.add(v)
            else:
                raise Exception("Categories input neither list nor string/integer")

            print "OK 2"

            # Delete existing keywords
            for k in service.servicekeywords_set.all():
                ServiceKeywords.objects.filter(pk=k.id).delete()
            # insert new ones
            keywords = payload['srv_keywords']
            if type(keywords) == list:
                for i in keywords:
                    if i is not None:
                        k = ServiceKeywords(service=Services.objects.get(pk=_service), title=i)
                        k.save()
            elif type(keywords) is str and not None:
                k = ServiceKeywords(service=Services.objects.get(pk=_service), title=i)
                k.save()

            print "OK 3"

            # Delete existing languages
            for k in service.servicelanguages_set.all():
                ServiceLanguages.objects.filter(pk=k.id).delete()
            # insert new ones
            languages = payload['srv_language']
            if type(languages) == list:
                for i in languages:
                    if i is not None:
                        l = ServiceLanguages(service=Services.objects.get(pk=_service), alias=i)
                        l.save()
            elif type(languages) is str and not None:
                l = ServiceLanguages(service=Services.objects.get(pk=_service), alias=i)
                l.save()
            
            print "OK 4"

            return JsonResponse({"state": True, "link": "/provider", 'id': _service})
        except Exception as e:
            return JsonResponse({"state": False})
        except:
             return JsonResponse({"state": False})

    def delete(self, request, alias=None):
        """ 
        Delete a service based on unique alias(title) 
        """

        try:
            # check request type
            assert isinstance(request, HttpRequest)
            # check if alias exist
            if alias == None:
                raise Exception("Invalid alias")
            _title = urllib.unquote_plus(alias)
            
            # check owner and provider role
            service = Services.objects.get(title=_title)
            #if request.session['id'] != service.owner:
            #    raise Exception("403")
            
            # delete keywords instances         
            ServiceKeywords.objects.filter(service__exact=service.id).delete()
            # delete languages instances
            ServiceLanguages.objects.filter(service__exact=service.id).delete()
            # -------- TODO: demo 2 -----------
            # delete technical support relationships
            #
            # delete categories link
            for category in service.categories.all():
                service.categories.remove(category)

            # remove instance
            try:
                service.delete()
            except ObjectDoesNotExist as ex:
                raise Exception(ex.args[0])
            return JsonResponse({"state": True, "redirect": "/provider"})
        except Exception as e:
            return JsonResponse({"state": False})
        except:
             return JsonResponse({"state": False})

@loginRequiredView
class ServiceUpdateView(View):
    def get(self, request, alias=None):
        """
        Load the HTML in case of service edit-mode
        """

        try:
            # define template
            template = 'app/consumers/services/item/update/index.html'
            # languages
            import pycountry

            # service and provider info
            _pk = request.session['id']
            user = Users.objects.get(pk=_pk)
            provider = Providers.objects.get(user_id=user.id)
            title = urllib.unquote_plus(alias)
            service = Services.objects.get(title=title)

            # Available types
            types = []
            types.append({'id': 'H', "description": 'Human Based'})
            types.append({'id': "M", "description": "Machine Based"})

            # cover images
            covers = getDefaultCoverList()

            # load template
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                    'alias': alias,
                    'username': request.session['username'],
                    'service': service,
                    'types': types,
                    'categories': Categories.objects.all().order_by('id'),
                    'covers': covers,
                    'charging_models': ChargingPolicies.objects.all(),
                    'currencies': pycountry.currencies,
                    'users': Users.objects.exclude(pk=_pk).order_by('email'),
                    'languages': pycountry.languages,
                    'keywords': ServiceKeywords.objects.filter(service=service.id),
                    #'selected_languages': service.servicelanguages_set.all()
                }))
        except: 
            print_exc()

@loginRequiredView
class UploadServiceMedia(View):

    def post(self, request, pk=None):
        """
        Upload files related to a service such as:
        the cover image, the logo and the software package
        """

        try:  
            try:
                if request.FILES['srv_logo']:
                    # store image
                    _image = request.FILES['srv_logo']
                    temp = _image.name.split('.')
                    _image.name = str(pk) + "." + str(temp[-1])
                    path = settings.MEDIA_ROOT+ "/app/services/images/" + _image.name
                    # remove file if exist
                    removeFileInExistance(path)
                    # store new file
                    storeFile(path, request.FILES['srv_logo'])
                    Services.objects.filter(pk=pk).update( image = _image)
            except:
                pass            

            temp, path = None, None
            
            try:
                if request.FILES['srv_software']:
                    # store cover
                    _sw = request.FILES['srv_software']
                    temp = _sw.name.split('.')
                    _sw.name = str(pk) + "." + str(temp[-1])
                    path = settings.MEDIA_ROOT+ "/app/services/packages/" + _sw.name
                    # remove file if exist
                    removeFileInExistance(path)
                    # store new file
                    storeFile(path, request.FILES['srv_software'])
                    Services.objects.filter(pk=pk).update(software = _sw )
            except:
                pass
            
            links = breadcrumbLinks(request)
            return JsonResponse({"state": True, "link": links["collection"]})
        except Exception as e:
            return JsonResponse({"state": False, "reason":e.args})            
        except:
                return JsonResponse({"state": "False2"})
   
def getDefaultCoverList():
    """ 
    Get a list of platform default covers images
    """
    covers = []
    try:
        import os
        path = settings.MEDIA_ROOT+ "/app/platform/"
        url = settings.MEDIA_URL + "app/platform/"
        for i in os.walk(path):
            for j in i[2]:
                extension = j.split('.')
                if extension[1] in  ["png", "jpg", "jpeg"]:
                    covers.append({'path': url+j, 'file': j})
        return covers
    except: 
        return covers
 
def storeFile(path, filename):
    try:
        with open(path, 'wb+') as destination:
            for chunk in filename.chunks():
                destination.write(chunk)
    except:
        pass
        
def removeFileInExistance(filepath):
    try:
        import os
        os.remove(filepath)
    except OSError:
        pass


def getDistance(lat1, lon1, lat2, lon2):
    """
    A(lat1, lon1) -> user
    B(lat2, lon2) -> service
    """
    
    try: 
        from math import sin, cos, pi, acos
        radlat1 = pi * lat1/180
        radlat2 = pi * lat2/180
        radlon1 = pi * lon1/180
        radlon2 = pi * lon2/180
        theta = lon1-lon2
        radtheta = pi * theta/180
        dist = sin(radlat1) * sin(radlat2) + cos(radlat1) * cos(radlat2) * cos(radtheta);
        dist = acos(dist)
        dist = dist * 180/pi
        dist = dist * 60 * 1.1515
        dist = dist * 1.609344
        return dist
    except: 
        return -1



#################################
## Services - consumers
#################################
class ServiceConsumerView(View):
    def get(self, request, alias=None):
        try:
            # define template
            template = 'app/consumers/search/services/preview.html'
            # languages
            import pycountry

            # service and provider info
            _pk = request.session['id']
            user = Users.objects.get(pk=_pk)
            provider = Providers.objects.get(user_id=user.id)
            title = urllib.unquote_plus(alias)
            service = Services.objects.get(title=title)

            # Available types
            types = []
            types.append({'id': 'H', "description": 'Human Based'})
            types.append({'id': "M", "description": "Machine Based"})

            # cover images
            covers = getDefaultCoverList()
            
            keywords = ServiceKeywords.objects.filter(service_id=service.id)
            if not keywords:
                keywords = None

            languages, langList = None, []
            import pycountry
            languages = ServiceLanguages.objects.filter(service_id=service.id)
            for l in pycountry.languages:
                for i in languages:
                    if i.alias == l.terminology:
                        langList.append(l.name)               

            # load template
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                    'alias': alias,
                    'username': request.session['username'],
                    'service': service,
                    'provider': Users.objects.get(pk=service.owner_id),
                    'keywords': keywords,
                    'languages': languages,
                    'categories': Categories.objects.all().order_by('id'),
                    'covers': covers,
                    'model': ChargingPolicies.objects.get(pk=service.charging_policy_id),
                    'rating': ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0],
                    'reviews': ConsumersToServices.objects.filter(service_id=service.id).count(),
                    'currencies': pycountry.currencies
                }))
        except: 
            pass

#################################
##  Technical support
#################################
class TechnicalSupport(View):
    def get(self, request):
        """
        Get the home page for technical support related topics in AoD platform
        """
        template = "app/help/index.html"
        try:
            assert isinstance(request, HttpRequest)
            
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Technical support',
                    'year':datetime.now().year,
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                }))
            
        except:
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Technical support',
                    'year':datetime.now().year,
                    'username': ''
                }))

class CreateAccountSupport(View):
    def get(self, request):
        """
        Load the page that describes step-by-step how a visitor can create a new account
        """
        template = "app/help/create_new_account.html"
        try:
            assert isinstance(request, HttpRequest)
            
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Technical support',
                    'year':datetime.now().year,
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                }))
            
        except:
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Technical support',
                    'year':datetime.now().year,
                    'username': ''
                }))

class LogInOutSupport(View):
    def get(self, request):

        template = "app/help/log-in-out.html"
        try:
            assert isinstance(request, HttpRequest)
            
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Technical support | Log in/out',
                    'year':datetime.now().year,
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request)
                }))
            
        except:
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Technical support',
                    'year':datetime.now().year,
                    'username': ''
                }))

class ForgetPasswordSupport(View):
    def get(self, request):

        template = "app/help/forget-password.html"
        try:
            assert isinstance(request, HttpRequest)
            
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Technical support | Forget password',
                    'year':datetime.now().year,
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                }))
        except:
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Technical support',
                    'year':datetime.now().year,
                    'username': ''
                }))

@loginRequiredView
class UpdateProfileSupport(View):
    def get(self, request):
        """
        Load the page that describes how a registered user can update his profile
        """
        template = "app/help/update-profile-steps.html"
        try:
            assert isinstance(request, HttpRequest)

            if 'username' in request.session:
                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'title':'Technical support | Update my profile',
                        'year':datetime.now().year,
                        'username': request.session["username"],
                        'links': navbarLinks(request),
                        'breadcrumb': breadcrumbLinks(request),
                    }))
        except:
            pass

@loginRequiredView
class ChangePasswordSupport(View):
    def get(self, request):
        """
        Load the page that describes how a registered user can change his password
        """
        template = "app/help/change-password.html"
        try:
            assert isinstance(request, HttpRequest)

            if 'username' in request.session:
                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'title':'Technical support | Change password',
                        'year':datetime.now().year,
                        'username': request.session["username"],
                        'links': navbarLinks(request),
                        'breadcrumb': breadcrumbLinks(request),
                    }))
        except:
            pass

@loginRequiredView
class RegisterServiceSupport(View):
    def get(self, request):
        """
        Load the page that describes how a registered user can upload a new service
        """
        template = "app/help/services/provider/create-service.html"
        try:
            assert isinstance(request, HttpRequest)

            if 'username' in request.session:
                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'title':'Technical support | Register service',
                        'year':datetime.now().year,
                        'username': request.session["username"],
                        'links': navbarLinks(request),
                        'breadcrumb': breadcrumbLinks(request),
                    }))
        except:
            pass

@loginRequiredView
class UpdateServiceSupport(View):
    def get(self, request):
        """
        Load the page that describes how a registered user can update an existing service
        """
        template = "app/help/services/provider/update-service.html"
        try:
            assert isinstance(request, HttpRequest)

            if 'username' in request.session:
                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'title':'Technical support | Update service',
                        'year':datetime.now().year,
                        'username': request.session["username"],
                        'links': navbarLinks(request),
                        'breadcrumb': breadcrumbLinks(request),
                    }))
        except:
            pass

@loginRequiredView
class DeleteServiceSupport(View):
    def get(self, request):
        """
        Load the page that describes how a registered user can delete an existing service
        """
        template = "app/help/services/provider/delete-service.html"
        try:
            assert isinstance(request, HttpRequest)

            if 'username' in request.session:
                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'title':'Technical support | Delete service',
                        'year':datetime.now().year,
                        'username': request.session["username"],
                        'links': navbarLinks(request),
                        'breadcrumb': breadcrumbLinks(request),
                    }))
        except:
            pass


#################################
##      Add to cart
#################################
@loginRequiredView
class CartView(View):
    def get(self, request):
        """
        Retrieve your personal cart 
        """
        
        template = "app/consumers/cart/index.html" 
        try:
            services = None
            providers = []
            if 'cart' in request.session:
                list = request.session["cart"]       
                services = Services.objects.filter(pk__in=list)
                for s in services:
                    u = Users.objects.get(pk=s.owner_id)
                    providers.append({'service': s.id, "owner": u.name + " " + u.lastname })
            
            print providers

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'My cart',
                    'year':datetime.now().year,
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
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


#################################
##      Consumer stats
#################################
@loginRequiredView
class MyStats(View):
    def get(self, request):
        """
        Retrieve your personal cart 
        """
        
        template = "app/consumers/statistics/index.html" 
        try:
            # get ConsumerID
            state, user, consumer = getConsumerInfo(request)
            print state
            #user = Users.objects.get(pk = request.session['id'])
            #consumer = Consumers.objects.get(user_id = user.id)

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'My collection',
                    'year':datetime.now().year,
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
                    'consumer': {"id": consumer.id, "info": user.name + " " + user.lastname}
                })
            )
        except:
            raise Http404


###############################################
## Network of assistance services - requests
###############################################
@loginRequiredView
class NetworkAssistanceServicesRequests(View):
    def get(self, request):
        """Load the page that includes the NAS requests"""

        template = "app/nas/requests/index.html" 

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
                    'title':'Network of assistance services',
                    'year': str(datetime.now().year),
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request),
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

        template = "app/nas/requests/create-new.html" 
        try:
            #load user
            pk = request.session['id']            

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Network of assistance services',
                    'year': str(datetime.now().year),
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request)
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
            from django.core.mail import send_mail, EmailMultiAlternatives
            subject = "[P4ALL] Network of assistance services notification"
            from_email = "no-reply@p4all.com"

            
            if settings.DEBUG:
                if settings.EVALUATION_PROCESS:
                    to = [settings.EVALUATION_EMAIL]
                else:
                    to = [settings.AOD_EMAIL]
            else:
                to = [receiver.email]

            # Create agree/disagree links
            domain =  request.scheme  + "://" +  request.META['HTTP_HOST'] 
            path = '/assistance/requests/reply'
            positiveLink = domain + path + "?rec=" + str(receiver.email) + "&sen=" + str(sender.email) + "&val=" + str(nasRequest.id) + "&code=true"
            negativeLink = domain + path + "?rec=" + str(receiver.email) + "&sen=" + str(sender.email) + "&val=" + str(nasRequest.id) + "&code=false"

            body = "<div>Dear <strong>" + receiver.name + " " + receiver.lastname + "</strong>,<br><br>"
            body += "The authorized AoD user, " + sender.name + " " + sender.lastname + ", requires privileges to setup your personal network of assistance services!<br>"
            body += "Do you want to grant permission on him/her?<br><br>"
            body += "If you agree, click here: <a href='" + positiveLink + " '>Yes, I do!</a><br><br>"
            body += "Otherwise, click here: <a href='"+negativeLink+"'>No, I do not agree</a><br><br>"
            body += "Sincerely,<br>The AoD administration team</div>"

            # send email with HTML code
            msg = EmailMultiAlternatives(subject, "", from_email, to)
            msg.attach_alternative(body, "text/html")
            msg.send()

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

                from django.core.mail import send_mail, EmailMultiAlternatives
                subject = "[P4ALL] Network of assistance services notification"
                from_email = "no-reply@p4all.com"
                
                if settings.DEBUG:
                    if settings.EVALUATION_PROCESS:
                        to = [settings.EVALUATION_EMAIL]
                    else:
                        to = [settings.AOD_EMAIL]
                else:
                    to = [receiver.email]
                
                # Inform the carer the consumer has replied on his/her request
                body = "<div>Dear <strong>" + carer.name + " " + carer.lastname + "</strong>,<br><br>"
                body += "The registered in AoD user, " + consumer.name + " " + consumer.lastname + ","
                if state == True:
                    body +=  " granted you with permission to setup his/her personal network of assistance services.<br>"
                else: 
                    body +=  " declined your request to setup his/her personal network of assistance services.<br>"
                body += "<br>Regards,<br>The AoD administration team</div>"

                # send email with HTML code
                msg = EmailMultiAlternatives(subject, "", from_email, to)
                msg.attach_alternative(body, "text/html")
                msg.send()

                #return redirect("/network-assistance-services/requests")
                return redirect(reverse('carer-landing-page'))

        except ObjectDoesNotExist:
            print("Model does not exist")
            return Http404
        except MultipleObjectsReturned:
            print("Multiple instances founded")
            return Http404
        except:
            return Http404


@loginRequiredView
class NetworkAssistanceServicesInviteCarers(View):

    def get(self, request):
        """ 
        Load the web page to send a new invitation on a carer
        """

        template = "app/nas/invitations/index.html" 
        try:
            #load user
            pk = request.session['id']            

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Invite carers',
                    'year': str(datetime.now().year),
                    'username': request.session["username"],
                    #'links': navbarLinks(request),
                    #'breadcrumb': breadcrumbLinks(request)
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
                from django.core.mail import send_mail, EmailMultiAlternatives
                subject = "[P4ALL] Network of carers: invitation"
                from_email = "no-reply@p4all.com"

            
                if settings.DEBUG:
                    if settings.EVALUATION_PROCESS:
                        to = [settings.EVALUATION_EMAIL]
                    else:
                        to = [settings.AOD_EMAIL]
                else:
                    to = [receiver.email]

                # Create agree/disagree links
                domain =  request.scheme  + "://" +  request.META['HTTP_HOST'] 
                path = '/assistance/invitations/reply'
                positiveLink = domain + path + "?rec=" + str(receiver.email) + "&sen=" + str(sender.email) + "&val=" + str(nasRequest.id) + "&code=true"
                negativeLink = domain + path + "?rec=" + str(receiver.email) + "&sen=" + str(sender.email) + "&val=" + str(nasRequest.id) + "&code=false"

                body = "<div>Dear " + receiver.name + " " + receiver.lastname + ",<br><br>"
                body += "The authorized AoD user, " + sender.name + " " + sender.lastname + ", wants to add you in his/her personal network of carers!<br>"
                body += "Do you want to grant permission on him/her?<br><br>"
                body += "If you agree, click here: <a href='" + positiveLink + " '>Accept</a><br><br>"
                body += "To decline it, click here: <a href='"+negativeLink+"'>Decline</a><br><br>"
                body += "Sincerely,<br>The AoD administration team</div>"
                
                # send email with HTML code
                msg = EmailMultiAlternatives(subject, "", from_email, to)
                msg.attach_alternative(body, "text/html")
                msg.send()

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

                from django.core.mail import send_mail, EmailMultiAlternatives
                subject = "[P4ALL] Network of carer: reply"
                from_email = "no-reply@p4all.com"
                
                if settings.DEBUG:
                    if settings.EVALUATION_PROCESS:
                        to = [settings.EVALUATION_EMAIL]
                    else:
                        to = [settings.AOD_EMAIL]
                else:
                    to = [receiver.email]
                
                # Advertise the carer's reply on consumer
                body = "<div>Dear " + consumer.name + " " + consumer.lastname + ",<br><br>"
                body += "The registered in AoD user, " + carer.name + " " + carer.lastname + ","
                if state == True:
                    body +=  " has accepted your invitation.<br>" +  carer.name + " is member of your personal network of carers.<br>"
                else: 
                    body +=  " has declined your invitation.<br>"
                body += "<br>Regards,<br>The AoD administration team</div>"

                # send email with HTML code
                msg = EmailMultiAlternatives(subject, "", from_email, to)
                msg.attach_alternative(body, "text/html")
                msg.send()

                #return redirect("/network-assistance-services/requests")
                return redirect(reverse('carer-landing-page'))

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



###############################################
## Setup Network of assistance services
###############################################
@loginRequiredView
class NetworkAssistanceServicesConfiguration(View):
    
    def get(self, request, consumer):
        """ 
        Load the web page to send a new request to assist a consumer with disability
        """

        template = "app/nas/configuration/index.html" 
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
                    'title':'Network of assistance services',
                    'year': str(datetime.now().year),
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request), 
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

                # retrieve temp selected services
                tempSelectedServices = NasTemporarySetup.objects.filter(carer_id=carer.id, consumer_id=consumer.id)
                tempSelectedServicesList = [i.service_id for i in tempSelectedServices]

                # already purchased services (by individual user)
                perUsagePolicy = ChargingPolicies.objects.filter(description__icontains="per usage")
                purchasedServicesList = [j.service_id for j in ConsumersToServices.objects.filter(consumer_id=consumer.id, is_completed=0)]

                # already purchased services (by carer)
                carerPurchasedServicesList = [c.service_id for c in NasConsumersToServices.objects.filter(consumer_id=consumer.id, is_completed=0)]

                # keep a list of unique IDs
                purchasedServicesList  = list(set(purchasedServicesList + carerPurchasedServicesList))

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
                        "purchased": (service.id in purchasedServicesList)
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
                #consumerId = request.GET.get('consumer_id')
                s2, consProfile, consumer = getConsumerInfo(request, request.GET.get('consumer_id'))

                # Retrieve the list of temporal selected instances (NasTemporarySetup model)
                tempServices = NasTemporarySetup.objects.filter(carer_id=carer.id, consumer_id=consumer.id)
                tempServicesList = [i.service_id for i in tempServices]

                # Group th categories based on relationship parent-child
                response = []
                for grandparent in Categories.objects.filter(category_id=None):
                    categoriesDict  = dict()
                    servicesIdList, servicesList    = [], []
                    categoriesDict["category"] = {"title": grandparent.title, "id": grandparent.id}

                    for parent in Categories.objects.filter(category_id=grandparent.id):
                        servicesIdList.append(parent.id)
                        for child in Categories.objects.filter(category_id=parent.id):
                            servicesIdList.append(child.id)
                  
                    # filter services and prepare response
                    for service in Services.objects.filter(pk__in=tempServicesList).filter(categories__id__in=servicesIdList):
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
                        })
                    categoriesDict['services'] = servicesList
                    response.append(categoriesDict)

                if settings.DEBUG == True:
                    print response
                
                return JsonResponse({"state": 1, "servicesList": response})
            else:
                return JsonResponse({"state": -1})
        except:
            if settings.DEBUG:
                print_exc()
            return JsonResponse({"state": -1})

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
        except: 
            print_exc()
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
                nas = NasConsumersToServices(     
                    service_id=payload['serviceID'],
                    purchased_date=datetime.now(),
                    consumer_id=consumer.id,
                    cost=selService.price
                )
                nas.save()
                curSrvId = nas.id

                # send email notification to consumer
                if settings.DEBUG:
                    if settings.EVALUATION_PROCESS:
                        to = [settings.EVALUATION_EMAIL]
                    else:
                        to = [settings.AOD_EMAIL]
                else:
                    to = [receiver.email]

                subject     = "[P4ALL] Network of assistance services: purchase service"
                body        = "<div>Dear <strong>" + receiver.name + " " + receiver.lastname + "</strong>,<br><br>"
                body        += "The authorized AoD user, " + carerProfile.name + " " + carerProfile.lastname + ", just purchased the service <em>"+selService.title+"</em> for you a few minutes ago!<br>"
                body        += "<br>Sincerely,<br>The AoD administration team</div>"
                sendEmail(carerProfile.email, to, subject, body, True)

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
                    purchasedServicesList = [j.service_id for j in ConsumersToServices.objects.filter(consumer_id=consumer.id, is_completed=0)]
                    # already purchased services (by carer)
                    carerPurchasedServicesList = [c.service_id for c in NasConsumersToServices.objects.filter(consumer_id=consumer.id, is_completed=0)]
                    # keep a list of unique IDs
                    purchasedServicesList  = list(set(purchasedServicesList + carerPurchasedServicesList))
                    # search for keywords in service title/description and service keywords
                    servicesKwdList = [k.service_id for k in ServiceKeywords.objects.filter(title__icontains=keyword).distinct()]

                    # retrieve services
                    services = Services.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(pk__in=servicesKwdList)).exclude(pk__in=purchasedServicesList).distinct()
                    data     = serializers.serialize("json", services)

                    return JsonResponse({"data": json.loads(data)})
            
                return JsonResponse({"data": []})
        except Exception as e:
            print e         
            return Http404

@loginRequiredView
class PreviewNetworkAssistanceServices(View):
    def get(self, request, consumer):
        try:
            assert isinstance(request, HttpRequest)
            pk = request.session['id']
            carer = Carers.objects.get(pk = pk)

            template = "app/nas/preview/index.html"
            
            targetUser  = Consumers.objects.get(user_id=consumer)
            targetProfile     = Users.objects.get(pk=consumer)
            
            selectedList = [s.service_id for s in NasTemporarySetup.objects.filter(carer_id=carer.id, consumer_id=targetUser.id)]
            selectedServicesList = Services.objects.filter(pk__in=selectedList)
                
            purchasedList = [p.service_id for p in NasConsumersToServices.objects.filter(consumer_id=targetUser.id)]
            purchasedServicesList = Services.objects.filter(pk__in=purchasedList)
                
            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title':'Network of assistance services preview',
                    'year': str(datetime.now().year),
                    'username': request.session["username"],
                    'links': navbarLinks(request),
                    'breadcrumb': breadcrumbLinks(request), 
                    'selectedServices': selectedServicesList,
                    'purchasedServices': purchasedServicesList,
                    'consumer': {'id': consumer, 'info': targetProfile.name + " " + targetProfile.lastname}
                }))
        except Exception as ex:
            print_exc()        
            return Http404


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




def sendEmail(sender, receiversList, subject, content, include_html):
    try:
        # send notification to activate his/her account
        sender = "no-reply@p4all.com"

        # send email with HTML code
        if include_html == True:
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, "", sender, receiversList)
            msg.attach_alternative(content, "text/html")
            msg.send()
        else:
            from django.core.mail import send_mail
            send_mail(subject, content, sender, receiversList, fail_silently=False)

    except Exception as e: 
        #import traceback        
        print e



#################################
##      TO fix them
#################################

def forgetPassword(request):
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/errors/404.html',
        context_instance = RequestContext(request,
        {
            'title':'Page no Found',
            'year':datetime.now().year,
        }))

def not_found(request):
    """ Handle the 404 http status """
    
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/errors/404.html',
        context_instance = RequestContext(request,
        {
            'title':'Page not Found',
            'year':datetime.now().year,
        }))

def method_not_allowed(request):
    """ Handle the 405 http status """

    assert isinstance(request, HttpRequest)
    return render(request,
        'app/errors/404.html',
        context_instance = RequestContext(request,
        {
            'title':'Internal server error',
            'year':datetime.now().year,
        }))

def server_error(request):
    """ Handle the 500 http status """

    assert isinstance(request, HttpRequest)
    return render(request,
        'app/errors/500.html',
        context_instance = RequestContext(request,
        {
            'title':'Internal server error',
            'year':datetime.now().year,
        }))
