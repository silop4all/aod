# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.views.generic import View

from app.models import Tokens
from app.microlabora import microlabora as ml
from app.decorators import loginRequiredView

from traceback import print_exc
import json
import logging
logger = logging.getLogger(__name__)


@loginRequiredView
class PublishMLTask(View):
    """Publish a human task in Microlabora (on demand)
    """

    def get(self, request):
        raise Http404

    def post(self, request):
        """Post the request to the microlabora web service and return its response
        """
        try:
            if request.is_ajax():
                if settings.OPENAM_INTEGRATION == False:
                    logger.warn("There is no integration with OpenAM. Check settings.py.")
                    return JsonResponse(data={"error": _("Unable to access the user profile from IAM")}, status=400)

                username = request.session.get('username', None)
                access_token = Tokens.objects.get(user_id=request.session['id']).access_token
                task = ml.Task(access_token)

                payload = json.loads(request.body)
                if 'UserId' not in payload:
                    payload['UserId'] = username

                (http_status, response_json) = task.publish(payload)
                return JsonResponse(data=response_json, status=200)

            return redirect(reverse('home_page'))
        except Exception as ex:
            logger.exception(str(ex))
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"error": str(ex)}, status=500)
