# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import (
    Http404, 
    HttpRequest, 
    HttpResponseServerError, 
    JsonResponse, 
    HttpResponse, 
    HttpResponseRedirect,
    HttpResponseForbidden
)
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import View

from app.models import (
    Users,
    Providers, 
    PaypalCredentials, 
    Services, 
    ServicePayment, 
    Tokens, 
    ConsumersToServices, 
    Consumers,
    ServiceRecurringPayment,
)
from app.decorators import loginRequiredView
from app.payment import p4a_payment, paypal
from app import utilities
from app.payment.config import __payment__

import ast
from datetime import datetime, timedelta
from traceback import print_exc
import json
import logging
logger = logging.getLogger(__name__)


@loginRequiredView
class PaymentSettings(View):

    def get(self, request):
        """Render the Payement settings of the provider"""

        try:
            template = "app/prosumers/provider-dashboard/payment/settings.html"
            provider = Providers.objects.get(user_id=request.session['id'])
            if provider.is_active == False:
                messages.info(request, "<span class='fa fa-exclamation-circle'></span> " + _("Only service providers are able to access their payment settings."))
                return redirect(reverse('home_page'), permanent=True) 

            settings = PaypalCredentials.objects.filter(provider=provider).first()

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'year': datetime.now().year,
                    'payment_settings': settings
                })
            )

        except Exception as ex:
            logger.exception(str(ex))
            return HttpResponseServerError(str(ex)) 


    def post(self, request):
        """Save the Paypal settings 0f each provider"""

        try:
            template = "app/prosumers/provider-dashboard/payment/settings.html"
            payload = request.POST

            if payload.get('username', None) in [None, ""]:
                raise IntegrityError(_("Please enter the Paypal client ID of your application"))
            if payload.get('password', None) in [None, ""]:
                raise IntegrityError(_("Please enter the Paypal client secret of your application"))                

            user = Users.objects.get(pk=request.session['id'])
            provider = Providers.objects.get(user_id=request.session['id'])
            settings = PaypalCredentials.objects.filter(provider=provider)

            insertion_flag = True
            if settings.count():
                insertion_flag = False
                settings.update(username=payload['username'], password=payload['password'])
            else:
                PaypalCredentials.objects.create(
                    provider=provider,
                    username=payload['username'],
                    password=payload['password']
                )

            # inform provider
            subject = "[P4ALL] Payment settings"
            content = "Dear " + user.username +",\n\n"
            if insertion_flag == True:
                content += "You have inserted successfully your payment settings in the AoD platform.\n\n"
            else:
                content += "You have modified your payment settings in the AoD platform.\n\n"
            content += "Let us know if this action has not been performed from your side!\n\n"
            content += "Sincerely,\nThe administration team"
            utilities.sendEmail([user.email], subject, content, False)                

            retrieve_paypal_access_token(request.session['id'])
            messages.info(request, _("Your settings haved been saved!"))
            return redirect(reverse('payment_settings'), permanent=True)

        except IntegrityError as ie:
            logger.exception(str(ie))
            messages.error(request, str(ie))
            return render(request, template,
                {
                    'year': datetime.now().year,
                    'payment_settings': payload
                }
            )
        except Exception as ex:
            logger.exception(str(ex))
            return HttpResponseServerError(str(ex)) 

@loginRequiredView
class PaymentCreateView(View):

    def post(self, request, pk):
        """Send a payment creation request after consumer action
        """
        try:
            # TODO: check integration with openam
            #if settings.OPENAM_INTEGRATION == False:
            #    return JsonResponse(data={"error": _("Unable to access the user profile from IAM")}, status=status.HTTP_400_BAD_REQUEST)

            service = Services.objects.get(pk=pk)       
            pd = ServicePayment.objects.get(service_id=service.id)                 
            total = float(service.price) + float(pd.tax) + float(pd.shipping) + float(pd.handling_fee)\
                + float(pd.shipping_discount) + float(pd.insurance)

            # IAM - access token
            access_token = Tokens.objects.get(user_id=request.session['id']).access_token
      
            # Paypal - access token
            paypal_token = retrieve_paypal_access_token(service.owner.user.id)
            if paypal_token is None or paypal_token == "":
                raise Exception("The Paypal token of the service provider is empty.")

            # prepare payment payload
            payload = {
                "intent": pd.payment_type,
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [
                    {
                        "amount": {
                            "total": str(total),
                            "currency": service.unit,
                            "details": {
                                "subtotal": str(service.price),
                                "tax": str(pd.tax),
                                "shipping": str(pd.shipping),
                                "handling_fee": str(pd.handling_fee),
                                "shipping_discount": str(pd.shipping_discount),
                                "insurance": str(pd.insurance)
                            }
                        },
                        "description": "Sale of service " + service.title + " at " + str(datetime.today().strftime("%Y-%m-%d %H:%M")) + ".",
                        "custom": "AoD_90048630024435",
                        "payment_options": {
                            "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
                        },
                        "soft_descriptor": "AOD-" + str(service.id),
                        "item_list": {
                            "items": [
                                {
                                    "name": service.title,
                                    "description": service.description,
                                    "quantity": "1",
                                    "price": str(service.price),
                                    "tax": str(pd.tax),
                                    "sku": "1",
                                    "currency": service.unit
                                }
                            ]
                        }
                    }
                ],
                "note_to_payer": "Contact us for any questions on your order.",
                "redirect_urls": {
                    "return_url": utilities.domainURL() + reverse('execute_paypal_payment', kwargs={'pk':pk}),
                    "cancel_url": utilities.domainURL() + reverse('cancel_paypal_payment', kwargs={'pk':pk})
                }
            }

            payment = p4a_payment.Payment(access_token, paypal_token)
            (http_status, response_json) = payment.create(payload)

            if int(http_status) == 201:
                link = ""
                links = response_json["payment"]["links"]
                for l in links:
                    if l['rel'] == "approval_url":
                        link = l['href']
                        break
                return redirect(link, permanent=True)
            else:
                logger.error('The creation of payment via payment component has failed with http status %s' % str(http_status))
                message = "<span class='fa fa-exclamation-circle'></span> " + _("Unable to proceed to payment process. Try again later or contact with the administrator")
                return redirect(reverse('service_view_page', kwargs={'pk':pk}))
        except Exception as ex:
            logger.exception(str(ex))
            message = "<span class='fa fa-exclamation-circle'></span> " + _("Unable to proceed to payment process. Try again later or contact with the administrator")
            messages.info(request, message)
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))

@loginRequiredView
class PaymentExecuteView(View):

    def get(self, request, pk):
        """Execute the payment after user approval.

        Paypal redirects user's browser here after the successful payment transaction.
        """

        try:
            query_params = request.GET
            service = Services.objects.get(pk=pk)  
            access_token = Tokens.objects.get(user_id=request.session['id']).access_token
            provider_id = Providers.objects.get(user_id=service.owner.user.id).id
            paypal_token = PaypalCredentials.objects.get(provider_id=provider_id).token

            transaction = ConsumersToServices.objects.create(
                consumer = Consumers.objects.get(user_id=request.session['id']),
                service_id = pk,
                payment_id = query_params.get("paymentId", None),
                paypal_user = query_params.get("PayerID", None), 
                purchased_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_completed = False
            )

            # invoke payment endpoint
            payment = p4a_payment.Payment(access_token, paypal_token)
            (http_status, response_json) = payment.execute(query_params.get("paymentId"), query_params.get("PayerID", None))

            consumer_to_service = ConsumersToServices.objects.filter(pk=transaction.id)
            if int(http_status) == 200:

                start_date = datetime.now()
                end_date = None
                if service.charging_policy_id == 2:
                    end_date = start_date + timedelta(minutes=15)
                    end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

                consumer_to_service.update(
                    is_completed=True, 
                    purchased_date=start_date.strftime("%Y-%m-%d %H:%M:%S"),
                    end_date=end_date,
                    access_resource=True
                )
                messages.info(request, _("Your payment has been completed successfully."))
            else:
                consumer_to_service.delete()
                messages.info(request, _("Your payment has been cancelled."))

            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))
        except Exception as ex:
            logger.critical(str(ex))
            messages.warning(request, _("Your payment has been skipped. An error has arisen."))
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))

@loginRequiredView
class PaymentCancelView(View):

    def get(self, request, pk):
        """Cancel the payment after user approval.
        Paypal redirects user's browser here after the cancellation of the payment transaction.

        :param request: the http request
        :type request: object
        :param pk: the service ID
        :type pk: integer        
        :returns: the HTTP response
        :rtype: object
        """
        try:
            query_params = request.GET

            payment_id = query_params.get("paymentId", None)
            consumer = Consumers.objects.get(user_id=request.session['id'])
            ConsumersToServices.objects.filter(service_id=pk, payment_id=payment_id, consumer=consumer).delete()
            messages.info(request, _("Your payment has been cancelled after your wish."))
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))
        except Exception as ex:
            logger.critical(str(ex))
            messages.info(request, _("Your payment has been cancelled after your wish."))
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))

@loginRequiredView
class BillingAgreementCreateView(View):

    def post(self, request, pk):
        """Create a billing agreement related to a service among service provider and consumer"""

        try:
            service = Services.objects.get(pk=pk) 
            recurring_payment = ServiceRecurringPayment.objects.get(service_id=pk)

            # IAM - access token
            access_token = Tokens.objects.get(user_id=request.session['id']).access_token
      
            # Paypal - access token
            paypal_token = retrieve_paypal_access_token(service.owner.user.id)
            if paypal_token is None or paypal_token == "":
                raise Exception("The Paypal token of the service provider is empty.")            

            # prepare billing agreement
            start_date = datetime.utcnow() + timedelta(hours=1)
            payload = {
                "name": "Service plan Agreement",
                "description": "Agreement for {} of the {} {}".format(service.title, service.owner.user.name, service.owner.user.lastname),
                "start_date": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "plan": {
                    "id": str(recurring_payment.plan_id)
                },
                "payer": {
                    "payment_method": "paypal",
                }
            }

            if settings.DEBUG:
                logger.debug(payload)

            billing_agreement = p4a_payment.BillingAgreement(access_token, paypal_token)
            (http_status, response_json) = billing_agreement.create(payload)

            if int(http_status) == 201:
                link = ""
                links = response_json["agreement"]["links"]
                for l in links:
                    if l['rel'] == "approval_url":
                        link = l['href']
                        break
                return redirect(link, permanent=True)
            else:
                logger.error('The creation of the recurring payment (billing aggrement) via payment component has failed with http status %s' % str(http_status))
                message = "<span class='fa fa-exclamation-circle'></span> " + _("Unable to proceed to recurring payment process. Try again later or contact with the administrator")
                return redirect(reverse('service_view_page', kwargs={'pk':pk}))
        except Exception as ex:
            logger.exception(str(ex))
            message = "<span class='fa fa-exclamation-circle'></span> " + _("Unable to proceed to recurring payment process. Try again later or contact with the administrator")
            messages.info(request, message)
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))

@loginRequiredView
class BillingAgreementExecuteView(View):
    """Handle the return url of the billing agreement"""

    def get(self, request, pk):
        """Execute the billing agreement after user approval.

        Paypal redirects user's browser here after the successful payment transaction.
        """
        try:
            query_params = request.GET
            service = Services.objects.get(pk=pk)  
            access_token = Tokens.objects.get(user_id=request.session['id']).access_token
            provider_id = Providers.objects.get(user_id=service.owner.user.id).id
            paypal_token = PaypalCredentials.objects.get(provider_id=provider_id).token

            transaction = ConsumersToServices.objects.create(
                consumer=Consumers.objects.get(user_id=request.session['id']),
                service_id=pk,
                purchased_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                is_completed=False
            )

            # invoke billing agreement execution endpoint
            billing_agreement = p4a_payment.BillingAgreement(access_token, paypal_token)
            (http_status, response_json) = billing_agreement.execute(query_params.get("token", None))

            consumer_to_service = ConsumersToServices.objects.filter(pk=transaction.id)
            if int(http_status) == 200:
                consumer_to_service.update(
                    is_completed=True, 
                    access_resource=True,
                    purchased_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
                    agreement_id=response_json["agreement"]["id"],
                    paypal_user=response_json["agreement"]["payer"]["payer_info"]["payer_id"]
                )
                messages.info(request, _("Your subscription has been completed successfully."))
            else:
                consumer_to_service.delete()
                messages.info(request, _("Your subscription has been cancelled."))

            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))
        except Exception as ex:
            logger.critical(str(ex))
            messages.warning(request, _("Your payment has been skipped. An error has arisen."))
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))

@loginRequiredView
class BillingAgreementSkipView(View):
    """Handle the cancel url of the billing agreement"""

    def get(self, request, pk):
        """Cancel the billing agrrement after user approval.
        Paypal redirects user's browser here after the cancellation of the payment transaction.
        """
        try:
            query_params = request.GET
            payment_token = query_params.get("token", None)
            messages.info(request, _("Your subscription has been cancelled after your wish."))
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))
        except Exception as ex:
            logger.critical(str(ex))
            messages.info(request, _("Your subscription has been cancelled after your wish."))
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))

@loginRequiredView
class BillingAgreementCancelView(View):
    """Handle the cancellation of the existing billing agreement, directly in Paypal"""

    def post(self, request, pk):

        try:
            user_id = request.session['id']
            service = Services.objects.get(pk=pk)  
            provider_id = Providers.objects.get(user_id=service.owner.user.id).id
            consumer_id = Consumers.objects.get(user_id=user_id).id
            consumer_to_services = ConsumersToServices.objects.filter(consumer_id=consumer_id, service=service).\
                filter(end_date__isnull=True, access_resource=True).exclude(agreement_id__isnull=True)
            consumer_to_service = consumer_to_services.first()

            token = retrieve_paypal_access_token(service.owner.user.id)
            billing_agreement = paypal.BillingAgreement(token) 
            (paypal_http_status, paypal_response) = billing_agreement.cancel(consumer_to_service.agreement_id)

            if int(paypal_http_status) == 204:
                ConsumersToServices.objects.filter(pk=consumer_to_service.id).update(end_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), access_resource=False)
                messages.info(request, _("Your subscription has been terminated successfully as you wish."))
            else:
                messages.info(request, _("Your cancallation of your subscription has not been performed. Try again later or contact with the administrator."))
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))    

        except Exception as ex:
            logger.critical(str(ex))
            messages.info(request, _("Your cancallation of your subscription has not been performed. Try again later or contact with the administrator."))
            return redirect(reverse('service_view_page', kwargs={'pk':pk} ))


def retrieve_paypal_access_token(user_id):
    """ Retrieve and store the access_token in paypal if user is merchant/provider
    """
    try:
        if not settings.PAYPAL_INTEGRATION:
            return None

        if Providers.objects.get(user_id=user_id).is_active == False:
            return None

        provider_id = Providers.objects.get(user_id=user_id).id
        try:
            provider_shop = PaypalCredentials.objects.get(provider_id=provider_id)
            if provider_shop:
                paypal_token = paypal.Token(provider_shop.username, provider_shop.password) 
                (paypal_http_status, paypal_response) = paypal_token.generate()
                if int(paypal_http_status) == 200:
                    PaypalCredentials.objects.filter(provider_id=provider_id).update(token=paypal_response["access_token"])
                    return paypal_response["access_token"]
                else:
                    # inform provider
                    user = Users.objects.get(pk=user_id)
                    subject = "[P4ALL] Payment settings"
                    content = "Dear " + user.username +",\n\n"
                    content += "Please validate the payment credentials that you have inserted in the AoD platform. It seems that something goes wrong!\n\n"
                    content += "Sincerely,\nThe administration team"
                    utilities.sendEmail([user.email], subject, content, False)
            raise Exception("")
        except:
            if settings.DEBUG:
                print_exc()
            logger.warning("Failed to retrieve the paypal access toekn for user %d" % user_id)
            raise Exception("")

    except Exception as ex:
        logger.exception(str(ex))
        if settings.DEBUG:
            print_exc()
        return None