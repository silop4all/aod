#import AoD models (inherit them from app application)
from app.models import *
# import AoD model serializers
from restapi.serializers import *

import sys

from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, filters, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer



@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'It_experience':        reverse('ItExperienceList', request=request, format=format),
        'Services':             reverse('ServicesList', request=request, format=format),
        'Charging_policies':    reverse('ChargingPoliciesList', request=request, format=format),
        'Categories':           reverse('CategoriesList', request=request, format=format),
        'Guided_network':       reverse('CarerAssistConsumerList', request=request, format=format),
        'Tags':                 reverse('CarerAssistConsumerList', request=request, format=format),
        'Services_congiguration':reverse('ServiceConfigurationList', request=request, format=format),
        'Members':              reverse('UsersList', request=request, format=format),
    })


class ItExperienceList(generics.ListAPIView):
    """
        Collection of IT skills
        ---
        GET:
            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
    """
    serializer_class = ItExperienceSerializer
    queryset = ItExperience.objects.all()    

class UsersList(generics.CreateAPIView):
    """
        Register user
        ---
        POST:
            omit_parameters:
              - form
            parameters:
              - name: JSON structure
                description: Create new user in AoD
                type: UserSerializer
                paramType: body
                pytype: UserSerializer

            responseMessages:
              - code: 201
                message: Created
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """
    serializer_class = UserSerializer
    queryset = Users.objects.all()


class UserRolesList(generics.ListAPIView):
    """
        Retrieve carers having specific email
        ---
        GET:
            parameters:
              - name: email
                description: Carer email account
                type: string
                paramType: query

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """

    serializer_class = UserRoleSerializer
    queryset = Users.objects.all()

    def get_queryset(self):
        email = self.request.query_params.get('email', None)
        carers = [c.user_id for c in Carers.objects.filter(is_active=1)]
        queryset = Users.objects.filter(email=email).filter(pk__in=carers)
        return queryset


class TagList(generics.ListAPIView):
    """
        Collection of tags (categories' metadata)
        ---
        GET 
            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
    """

    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class CategoriesList(generics.ListCreateAPIView):
    """
        Collection of categories
        ---
        GET:
            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml

        POST:
            omit_parameters:
              - form
            parameters:
              - name: JSON structure
                description: Create new category in AoD
                type: CategorySerializer
                paramType: body
                pytype: CategorySerializer

            responseMessages:
              - code: 201
                message: Created
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

class TreeCategoriesList(generics.ListAPIView):
    """
        Tree categories
        ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: level
                description: Zero for categories layer-1
                type: integer
                paramType: query

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
    """
    serializer_class = TreeCategorySerializer

    def get_queryset(self):
        queryset = Categories.objects.all()
        level = self.request.query_params.get('level', None)
        # root
        if level is not None:
            return queryset.filter(category__isnull=True)
        else:
            return queryset

class CategoriesResource(generics.RetrieveDestroyAPIView):
    """
        Category resource
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true
            
            responseMessages:
              - code: 200
                message: OK
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml

        DELETE:
            omit_serializer: true

            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true

            responseMessages:
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error
    """

    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    lookup_field = ('pk')

class ChargingPoliciesList(generics.ListAPIView):
    """
        Collection of charging methods
        ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: search
                description: Search based on keywords
                type: string
                paramType: query

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
    """
    queryset = ChargingPolicies.objects.all()
    serializer_class = ChargingPolicySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields   = ('name', 'description')


class ServicesList(generics.ListCreateAPIView):
    """
    Collection of services
        ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: search
                description: Search services based on keywords
                type: string
                paramType: query
              - name: ordering
                description: Ordering criterion
                type: string
                paramType: query
              - name: type
                description: Filter services based on the type (H or M)
                type: string
                paramType: query
              - name: charging_policy
                description: Filter services based on the charging_policy
                type: integer
                paramType: query

            responseMessages:
              - code: 200
                message: OK
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml

        POST:
            omit_parameters:
              - form

            parameters:
              - name: service
                description: Register a new service in AoD
                type: ServiceSerializer
                paramType: body
                pytype: ServiceSerializer

            responseMessages:
              - code: 201
                message: Created
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml

    """
    queryset            = Services.objects.all()
    serializer_class    = ServiceSerializer

    filter_backends     = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields       = ('type',  'charging_policy')
    search_fields       = ('title', 'description')
    ordering_fields     = ('title', 'created_date')

class ServicesResource(generics.RetrieveUpdateDestroyAPIView):
    """
        Service resource
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml

        PUT:
            omit_parameters:
              - form

            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true
              - name: service
                description: Update existing service
                type: ServiceSerializer
                paramType: body
                pytype: ServiceSerializer

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml


        PATCH:
            omit_parameters:
              - form

            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true
              - name: software
                paramType: body
                type: file
                description: Software resource
              - name: image
                paramType: body
                type: file
                description: Service image

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            consumes:
              - multipart/form-data 
            produces:
              - application/json
              - application/xml

        DELETE:
            omit_serializer: true

            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true

            responseMessages:
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error
    """

    serializer_class = ServiceSerializer
    queryset = Services.objects.all()
    lookup_field = ('pk')

class DetailedServiceResource(generics.RetrieveAPIView):
    """
        Detailed information per service
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """

    serializer_class = DetailedServiceSerializer
    queryset = Services.objects.all()
    lookup_field = ('pk')

class ServiceConfigList(generics.RetrieveAPIView):
    """
       Zero configuration collection per service 
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """

    serializer_class = ServiceConfigurationsSerializer
    queryset = Services.objects.all()
    lookup_field = ('pk')

class ServiceLanguagesList(generics.RetrieveAPIView):
    """
       Supported languages collection per service
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """

    serializer_class = ServiceLanguagesSerializer
    queryset = Services.objects.all()
    lookup_field = ('pk')

class ServiceTechnicalSupportList(generics.RetrieveAPIView):
    """
       Provided technical support per service
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Service Primary key
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """

    serializer_class = ServiceTechicalSupportSerializer
    queryset = Services.objects.all()
    lookup_field = ('pk')

class ServiceKeywordsList(generics.RetrieveAPIView):
    """
       Related keywords per service
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Service Primary key
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """

    serializer_class = ServiceKeywordsSerializer
    queryset = Services.objects.all()
    lookup_field = ('pk')

class SupportedLanguagesResource(generics.ListAPIView):
    """
        Service resource
        ---
        GET:

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """

    serializer_class = ServiceLanguagesSerializer
    queryset = ServiceLanguages.objects.all()

class ServiceReviewsList(generics.ListAPIView):
    """
    Retrieve reviews for a service
    ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: service
                paramType: path
                type: integer
                description: Primary key
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """
    serializer_class = ServiceReviewsSerializer
    queryset = ConsumersToServices.objects.all()

    def get_queryset(self):
        service = self.kwargs['service']
        queryset = ConsumersToServices.objects.filter(service=service)
        return queryset


class ServiceConfigurationList(generics.UpdateAPIView):
    """
    Update configuration
    ---
        PUT:
            omit_parameters:
              - form

            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
                required: true
              - name: service
                description: Update existing service
                type: ConfigurationSerializer
                paramType: body
                pytype: ConfigurationSerializer

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """
    serializer_class = ConfigurationSerializer
    queryset = ServiceConfiguration.objects.all()
    lookup_field = ('pk')


class ConsumerServicesList(generics.ListAPIView):
    """
    Service details for specific consumer
    ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: pk
                paramType: path
                type: integer
                description: User id
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """
    serializer_class = ConsumerServicesSerializer
    queryset = ConsumersToServices.objects.all()

    def get_queryset(self):
        consumer = self.kwargs['pk']
        queryset = ConsumersToServices.objects.filter(consumer=consumer)
        return queryset



# Assistance
class ConsumerAssistServicesList(generics.ListAPIView):
    """
    Service details for specific consumer
    ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: pk
                paramType: path
                type: integer
                description: User id
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """
    queryset = NasConsumersToServices.objects.all()
    serializer_class = ConsumerAssistServicesSerializer
    
    def get_queryset(self):
        user = self.kwargs['pk']
        #consumer = Consumers.objects.get(user_id=user)
        #queryset = NasConsumersToServices.objects.filter(consumer=consumer.id)
        consumer = self.kwargs['pk']
        queryset = NasConsumersToServices.objects.filter(consumer=consumer)
        return queryset

class ConsumerAssistServicesConfigurationList(generics.ListAPIView):
    """
       Zero configuration collection per service 
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Consumer id
                required: true
              - name: service
                paramType: path
                type: integer
                description: Service id
                required: true


            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
              - application/xml
              - application/yaml
    """

    serializer_class = ConsumerAssistServicesConfigurationSerializer
    queryset = NasConsumersToServices.objects.all()

    def get_queryset(self):
        user = self.kwargs['pk']
        consumer = Consumers.objects.get(user_id=user)
        service = self.kwargs['service']
        queryset = NasConsumersToServices.objects.filter(consumer=consumer.id).filter(service=service)
        return queryset

class AssistanceConfigurationList(generics.CreateAPIView):
    """
    Insert service configuration per consumer
    ---
        POST:
            omit_parameters:
              - form

            parameters:
              - name: service configuration
                description: Insert service configuration per consumer
                type: AssistanceConfigurationSerializer
                paramType: body
                pytype: AssistanceConfigurationSerializer

            responseMessages:
              - code: 201
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """
    serializer_class = AssistanceConfigurationSerializer
    queryset = NasConfiguration.objects.all()
    lookup_field = ('pk')


