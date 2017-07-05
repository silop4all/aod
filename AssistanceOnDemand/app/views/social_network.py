
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.views.generic import View

from app.models import Users, Tokens
from app.decorators import loginRequiredView

from traceback import print_exc
from md5 import md5
import urllib
import json
import logging
logger = logging.getLogger(__name__)



@loginRequiredView
class AccessSocialNetwork(View):
    
    def get(self, request):
        """Redirect the user in the social networking app
        """
        try:        
            pk = request.session['id']
            username = request.session['username']
            user = Users.objects.get(pk=pk)
            lang = str(self.request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)) if settings.LANGUAGE_COOKIE_NAME in self.request.COOKIES else settings.LANGUAGE_CODE

            if settings.OPENAM_INTEGRATION:
                token = Tokens.objects.get(user_id=pk)
                query_params = '?email=%s&info=%s&lang=%s' % (str(urllib.quote_plus(user.email)),str(token.access_token), lang)
            else: 
                hash = md5(str(pk))
                query_params = '?email=%s&info=%s&lang=%s' % (str(urllib.quote_plus(user.email)),str(hash.hexdigest()), lang)
            return redirect(settings.SOCIAL_NETWORK_URL + query_params)
        except ObjectDoesNotExist as e:
            logger.warn(str(e))
            if settings.DEBUG:
                print_exc()
            return Http404
        except Exception as ex:
            logger.exception(str(ex))
            if settings.DEBUG:
                print_exc()
            return Http404

