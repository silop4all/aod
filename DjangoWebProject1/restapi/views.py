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
        'It_experience':    reverse('ItExperienceList', request=request, format=format),
        'Services':         reverse('ServicesList', request=request, format=format),
        'Charging_policies':reverse('ChargingPoliciesList', request=request, format=format),
        'Categories':       reverse('CategoriesList', request=request, format=format),
        'Guided_network':   reverse('CarerAssistConsumerList', request=request, format=format),
        'Tags':             reverse('CarerAssistConsumerList', request=request, format=format),
        'Services_congiguration':  reverse('ServiceConfigurationList', request=request, format=format),
        'Members':          reverse('UsersList', request=request, format=format),
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
    parser_classes = (JSONParser, XMLParser,)
    renderer_classes = (JSONRenderer, XMLRenderer,)


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

    parser_classes      = (JSONParser, XMLParser,)
    renderer_classes    = (JSONRenderer, XMLRenderer,)


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
    parser_classes = (JSONParser, XMLParser,)
    renderer_classes = (JSONRenderer, XMLRenderer,)


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
    parser_classes = (JSONParser, XMLParser,)
    renderer_classes = (JSONRenderer, XMLRenderer,)


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
    parser_classes = (JSONParser, XMLParser,)
    renderer_classes = (JSONRenderer, XMLRenderer,)
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
    parser_classes = (JSONParser, XMLParser,)
    renderer_classes = (JSONRenderer, XMLRenderer,)
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

    parser_classes      = (JSONParser, XMLParser,)
    renderer_classes    = (JSONRenderer, XMLRenderer,)

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

        PUT:
            omit_parameters:
              - form

            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key
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

    parser_classes      = (JSONParser, XMLParser,)
    renderer_classes    = (JSONRenderer, XMLRenderer,)


class ServiceConfigurationList(generics.ListCreateAPIView):
    serializer_class = ServiceConfigurationSerializer
    queryset = ServiceConfiguration.objects.all()
    lookup_field = ('pk')

    parser_classes      = (JSONParser, XMLParser,)
    renderer_classes    = (JSONRenderer, XMLRenderer,)










class CarerAssistConsumerList(generics.ListCreateAPIView):
    """
    Get a collection of permissions requests for the guided network 
    """
    queryset = CarersAssistConsumers.objects.all()
    serializer_class = CarerAssistSerializer