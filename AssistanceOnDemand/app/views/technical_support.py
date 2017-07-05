# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from django.http import Http404, JsonResponse, HttpResponseServerError, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.utils.translation import ugettext as _

from app.models import *
from app.decorators import loginRequiredView
from app.utilities import sendEmail

from traceback import print_exc
from datetime import datetime
from pycountry import currencies
import json
import logging
logger = logging.getLogger(__name__)


class FAQTopicListView(View):

    def get(self, request):
        """
        Retrieve a list of available FAQ topics with their related articles
        """
        try:
            template = "app/technical-support/index.html" 

            topicList = list()
            for i in Topic.objects.filter(visible=True):
                articlesList = list()
                q = i.articles.filter(visible=True)
                for j in q:
                    articlesList.append({"id": j.id, "title": j.title, "link": reverse('faq_article', kwargs={"pk": j.id}) } )
                topicList.append({"id": i.id, "title": i.title, 'articles_num': q.count(), "articles": articlesList })

            if settings.DEBUG:
                print topicList

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Frequently Asked Questions'),
                    'year': str(datetime.now().year),
                    'topic_list': topicList,
                }))
        except Exception as ex:
            logger.exception(str(ex))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

class FAQTopicView(View):

    def get(self, request, pk):
        """
        Retrieve a specific FAQ topic with the related articles
        """
        try:
            template = "app/technical-support/topics/index.html" 
            topic = Topic.objects.get(pk=pk)

            if topic.protected and "id" not in request.session.keys():
                return redirect(reverse('login_page'))

            if topic.visible == True: 
                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'title': _(' FAQ - '),
                        'year': str(datetime.now().year),
                        'username': request.session["username"] if "username" in request.session else None,
                        'topic': topic
                    }))
            else:
                raise Http404
        except Exception as ex:
            logger.exception(str(ex))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

class FAQArticleView(View):

    def get(self, request, pk):
        """
        Retrieve a specific FAQ article 
        """
        try:
            template = "app/technical-support/topics/articles/index.html" 
            article = Article.objects.get(pk=pk)

            if article.protected and "id" not in request.session.keys():
                return redirect(reverse('login_page'))

            community_members = PlatformCommunityMember.objects.exclude(is_active=False)
            community_volunteers = community_members.filter(is_volunteer=True)
            community_professionals = community_members.filter(is_professional=True)

            if article.visible == True: 
                return render(request, template,
                    context_instance = RequestContext(request,
                    {
                        'title': _(' FAQ - ') + article.title,
                        'year': str(datetime.now().year),
                        'article': article,
                        'logged_user': Users.objects.get(pk=request.session['id']) if 'id' in request.session.keys() else None,
                        "contact_us": ContactUs.objects.get(active=True),
                        "community_members": community_members,
                        "community_volunteers": community_volunteers,
                        "community_professionals": community_professionals
                    })
                )
            else:
                 raise Http404
        except Exception as ex:
            logger.exception(str(ex))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

@loginRequiredView
class CommunitiesListView(View):

    def get(self, request):
        """Retrieve a list of communities """
        try:
            template = "app/technical-support/communities/list.html" 

            enhanced_community_list = []
            communities_list = Community.objects.filter(is_active=True)
            for c in communities_list:
                d = dict()
                cm = CommunityMember.objects.filter(community_id=c.id, user_id=request.session['id'])
                if cm.count():
                    is_active_member = cm[0].is_active
                    is_owner = cm[0].is_owner

                    d['is_active_member'] = cm[0].is_active
                    d['is_owner'] = cm[0].is_owner
                d['id'] = c.id
                d['title'] = c.title
                d['service'] = c.service_id
                d['ref_service'] = c.ref_service
                d['created_at'] = c.created_at
                enhanced_community_list.append(d)

            # check if aod community member
            aod_community_member = None
            aod_community_members = PlatformCommunityMember.objects.filter(user_id=request.session['id'])
            if aod_community_members.count() > 0:
                aod_community_member = aod_community_members[0]

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Communities'),
                    'year': str(datetime.now().year),
                    'communities_list': enhanced_community_list,
                    'aod_community_member': aod_community_member,
                }))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

@loginRequiredView
class CommunitiesView(View):

    def get(self, request):
        """Render the form for the management of a community details"""
        try:
            template = "app/technical-support/communities/index.html" 

            # Find services with community
            supported_services_list = Community.objects.all().values_list('ref_service_id', flat=True)

            # Fetch the human or machine services that allow community support, is visible without existing community
            # Allow at most one community per human or machine service 
            services_list = Services.objects.filter(community_support=True, is_visible=True).\
                exclude(pk__in=supported_services_list).order_by('title')

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Initiate a community based service'),
                    'year': str(datetime.now().year),
                    'services_list': services_list,
                    'currency_list': currencies,
                }))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

    def post(self, request):
        """Initiate a community to support a service"""

        try:
            user_id = request.session['id']
            community_type = dict(COMMUNITY_CHOICES)
            payload = request.POST

            role = payload.get('role', None)
            if role == None:
                raise ObjectDoesNotExist("Role is not acceptable")
            if int(role) == 1:
                is_volunteer = True,
                is_professional = False
            else:
                is_volunteer = False
                is_professional = True

            fee = None
            if payload.get('fee') == u'':
                fee = None
            else:
                fee = float(payload.get('fee'))

            # create community-based service
            community_service = Services(
                title = payload.get('title', None),
                description = payload.get('description', None),
                image = "",
                type = community_type.keys()[0],
                charging_policy_id = 1, # set free
                owner = Providers.objects.get(user_id=user_id),
                language_constraint = False,
                location_constraint = False,
                is_visible = True,
                community_support = False
            )
            community_service.save()

            # Add categories that service supports
            for c in Services.objects.filter(pk=payload.get('ref_service')).values_list('categories', flat=True):
                community_service.categories.add(c)

            # Create community (link among services)
            community = Community(
                title = payload.get('title', None),
                service_id = community_service.id,
                ref_service_id = payload.get('ref_service', None),
                is_active = True
            )
            community.save()

            # Add owner of the community
            community_owner = CommunityMember(
                community_id = community.id,
                user= Users.objects.get(pk=user_id),
                is_owner = True,
                is_volunteer = is_volunteer,
                is_professional = is_professional,
                fee = fee,
                currency = payload.get('currency', None),
                is_active = True,
                skype = payload.get('skype', None)
            )
            community_owner.save()

            # Send email notification towards AoD admin
            content = _("Dear admin,\n\nA new community has been initiated from my side to support the service %s.\n\nBest regards,\n%s")\
                    % (community.title, request.session['username'])
            sendEmail([settings.DEVELOPER_EMAIL], _("[P4ALL] Initiate new community"), content, False)

            # Send email notifications towards users that have declared their interest to participate in communities
            content = _("Dear users,\n\nA new community has been initiated for the service %s.\n\nBest regards,%s\n")\
                    % (community.ref_service.title, request.session['username'])
            email_list = Users.objects.filter(community_participation=True).values_list('email', flat=True)
            if len(email_list) > 0:
                sendEmail(email_list, _("[P4ALL] Community notification"), content, False)

            return redirect(reverse('communities_list'))

        except IntegrityError as ie:
            logger.exception(str(ie))
            return Http404
        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

@loginRequiredView
class CommunityMembersView(View):

    def get(self, request, pk=None):
        """Retrieve the members of a community"""
        try:
            template = "app/technical-support/communities/members.html" 

            user_id = request.session['id']
            community = Community.objects.get(pk=pk)
            if not CommunityMember.objects.get(community_id=community.id, user_id=user_id).is_owner:
                return HttpResponseForbidden()

            members_list = CommunityMember.objects.filter(community_id=community.id)

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Community members'),
                    'year': str(datetime.now().year),
                    'community': community,
                    'members_list': members_list,
                }))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

@loginRequiredView
class JoinCommunityView(View):
    
    def get(self, request, pk=None):
        """Load template to submit the request (join in community of interest)"""
        try:
            template = "app/technical-support/communities/members/requests.html" 

            user_id = request.session['id']
            community = Community.objects.get(pk=pk)

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Join to community'),
                    'year': str(datetime.now().year),
                    'community': community,
                    'currency_list': currencies,
                }))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

    def post(self, request, pk=None):
        """Require access to become member of community"""
    
        try:
            user_id =request.session['id']
            payload = request.POST

            if settings.DEBUG:
                print payload

            community_owner = CommunityMember.objects.get(community_id=pk, is_owner=True).user_id
            owner = Users.objects.get(pk=community_owner)

            fee = None
            if payload.get('fee') == u'':
                fee = None
            else:
                fee = float(payload.get('fee'))

            role = payload.get('role', None)
            if role == None:
                raise ObjectDoesNotExist("Role is not acceptable")
            if int(role) == 1:
                is_volunteer = True,
                is_professional = False
            else:
                is_volunteer = False
                is_professional = True

            # Add a member in community with pending status
            member = CommunityMember(
                community_id = pk,
                user_id = user_id,
                is_owner = False,
                message = payload.get('message', None),
                fee = fee,
                currency = payload.get('currency', None),
                is_active = None,
                is_professional = is_professional,
                is_volunteer = is_volunteer,
                skype = payload.get('skype', None)
            )
            member.save()
            
            community = Community.objects.get(pk=member.community_id)
            service = Services.objects.get(pk=community.service_id)

            # Send email notifications towards owner
            content = _("Dear %s,\n\nI would like to become member of the %s community. Please accept my request.\n\nBest regards,\n%s")\
                    % (owner.username, service.title, request.session['username'])
            sendEmail([owner.email], _("[P4ALL] Join to community request"), content, False)

            return redirect(reverse('communities_list'))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

@loginRequiredView
class LeaveCommunityView(View):

    def get(self, request, pk=None):
        """Leave from specific community"""
    
        try:
            user_id =request.session['id']

            community_member = CommunityMember.objects.get(community_id=pk, is_owner=True)
            owner = Users.objects.get(pk=community_member.user_id)
            community = Community.objects.get(pk=pk)

            CommunityMember.objects.get(community_id=pk, user_id=user_id).delete()

            # Send email notification towards community owner
            content = _("Dear %s,\n\nI have decided to leave from the %s community.\n\nBest regards,\n%s")\
                    % (owner.username, community.title, request.session['username'])
            sendEmail([owner.email], _("[P4ALL] Leave from community"), content, False)

            return redirect(reverse('communities_list'))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

@loginRequiredView
class SetCommunityMemberView(View):

    def get(self, request,community=None, member=None):
        raise Http404

    def post(self, request, community=None, member=None):
        """Community owner can update the status of a (wanna be) member"""
        try:
            template = "app/technical-support/communities/members.html" 

            # community owner authorization
            if not CommunityMember.objects.get(community_id=community, user_id=request.session['id']).is_owner:
                return HttpResponseForbidden()

            if request.is_ajax():
                body = ""
                payload = json.loads(request.body)
                future_member = Users.objects.get(pk=member)
                service_id = Community.objects.get(pk=community).service_id
                service = Services.objects.get(pk=service_id)

                if payload['status']:
                    CommunityMember.objects.filter(community_id = community, user_id = member).update(is_active = payload['status'])
                    body = "Your request for the participation in the community of the service %s has been accepted." % service.title
                else:
                    CommunityMember.objects.filter(community_id = community, user_id = member).delete()
                    body = "Your request for the participation in the community of the service %s  been rejected." % service.title

                # Send email notification towards user that require access in community            
                content = "Dear %s,\n\n%s\n\nThe community owner,\n%s" % (future_member.username, body, request.session['username'])
                sendEmail([future_member.email], _("[P4ALL] Join to community response"), content, False)

                return JsonResponse({"link": reverse('community_members', kwargs={'pk':community})})

            else: 
                return redirect(reverse('community_members', kwargs={'pk':community}))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

@loginRequiredView
class PlatformCommunityRequestView(View):
    
    def get(self, request,):
        """Load template to submit the request (join in aod community)"""
        try:
            template = "app/technical-support/platform/requests.html" 

            return render(request, template,
                context_instance = RequestContext(request,
                {
                    'title': _('Join to AoD community support'),
                    'year': str(datetime.now().year),
                    'currency_list': currencies,
                }))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()

    def post(self, request):
        """Require access to the platform community"""
    
        try:
            payload = request.POST
            user_id =request.session['id']
            user = Users.objects.get(pk= user_id)

            fee = None
            if payload.get('fee') == u'':
                fee = None
            else:
                fee = float(payload.get('fee'))

            role = payload.get('role', None)
            if role == None:
                raise ObjectDoesNotExist("Role is not acceptable")
            if int(role) == 1:
                is_volunteer = True,
                is_professional = False
            else:
                is_volunteer = False
                is_professional = True

            community_member = PlatformCommunityMember(
                user = Users.objects.get(pk=user_id),
                message = payload.get('message', None),
                fee = fee,
                currency = payload.get('currency', None),
                is_professional = is_professional,
                is_volunteer = is_volunteer,
                skype = payload.get('skype', None)
            )
            community_member.save()

            # notify admin via email
            content = _("Dear admin,\n\nI would like to become member of you platform community. Please accept my request.\n\nSincerely,\n%s")\
                    % (request.session['username'])
            sendEmail([user.email], _("[P4ALL] Join to platform community"), content, False)

            return redirect(reverse('communities_list'))

        except ObjectDoesNotExist as oe:
            logger.error(str(oe))
            raise Http404
        except Exception as e:
            logger.exception(str(e))
            if settings.DEBUG:
                print_exc()
            return HttpResponseServerError()
