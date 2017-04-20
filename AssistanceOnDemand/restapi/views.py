import re
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

from drf_multiple_model.views import MultipleModelAPIView

from app.models import *
from restapi.serializers import *


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

    serializer_class = ServiceLanguagesListSerializer
    queryset = Services.objects.all()
    lookup_field = ('pk')

class ServiceMaterialsList(generics.RetrieveAPIView):
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

class ServiceMaterialResource(generics.RetrieveAPIView):
    """
       Provided technical support per service
        ---
        GET:
            parameters:
              - name: pk
                paramType: path
                type: integer
                description: Primary key of technical support material 
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

    serializer_class = ServiceTechnicalSupportSerializer
    queryset = ServicesToTechnicalSupport.objects.all()
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

    serializer_class = ServiceKeywordsListSerializer#ServiceKeywordsSerializer
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


class ArticlesList(generics.ListAPIView):
    """
        Retrieve public articles in topic
        ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: topic
                description: The ID of the target topic
                type: string
                paramType: url

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

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """

    serializer_class = ArticleSerializer

    def get_queryset(self):
        topic_id = self.kwargs['topic']
        queryset = Article.objects.filter(topic_id=topic_id, visible=True)
        return queryset

class PublishQuestionList(generics.CreateAPIView):
    """
        Publish user question to application's admin
        ---
        POST:
            omit_parameters:
              - form
            parameters:
              - name: JSON structure
                description: Publish question in AoD
                type: PublishQuestionSerializer
                paramType: body
                pytype: PublishQuestionSerializer

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
    serializer_class = PublishQuestionSerializer
    queryset = IncomingQuestions.objects.all()

class SearchEngine(generics.ListAPIView):
    """
        Default AoD seaech engine
        ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: owners
                description: Filter services based on providers
                type: string
                paramType: query
              - name: categories
                description: Filter services based on categories
                type: string
                paramType: query
              - name: types
                description: Filter services based on the type (H or M)
                type: string
                paramType: query
              - name: models
                description: Filter services based on the free (1) or paid policy (0)
                type: integer
                paramType: query
              - name: distance
                description: Filter services based on distance from lat and lon
                type: float
                paramType: query
              - name: lat
                description: Current latitude 
                type: float
                paramType: query
              - name: lon
                description: Current longitude 
                type: float
                paramType: query
              - name: minQoS
                description: Filter services based on minimum QoS
                type: float
                paramType: query
              - name: maxQoS
                description: Filter services based on maximum QoS
                type: float
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

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """

    serializer_class = ServiceSerializer

    def get_queryset(self):
        from app import utilities
        from django.db.models import Avg

        query = self.request.query_params
        servicesList = Services.objects.all()

        #  Filter services based on their providers
        if 'owners' in query:
            if query.get('owners', None) not in ["", "null", None]:
                owners = str(query.get('owners', None)).split(',')
                owners = map(int, owners)
                if  type(owners) is list and len(owners):
                    servicesList = servicesList.filter(owner_id__in=owners)

        # Filter services based on categories
        if 'categories' in query:
            categories = str(query.get('categories', None)).split(',')
            categories = map(int, categories)
            if  type(categories) is list and len(categories):
                servicesList = servicesList.filter(categories__pk__in=categories)

        # Filter services based on types
        if 'types' in query:
            types = str(query.get('types', None)).split(',')
            if  type(types) is list and len(types):
                servicesList = servicesList.filter(type__in=types)

        # Filter services based on charging models
        if 'models' in query:
            models = str(query.get('models', None)).split(',')
            models = map(int, models)

            # Map: free->1, paid->0
            if type(models) is list and len(models):
                if models == [1]:
                    servicesList = servicesList.filter(charging_policy_id=1)
                elif models == [0]:
                    servicesList = servicesList.exclude(charging_policy_id=1)
                    if 'minPrice' in query and query.get("minPrice") not in ["", None]:
                        servicesList = servicesList.filter(price__gte=float(query.get("minPrice")))
                    if 'maxPrice' in query and query.get("maxPrice") not in ["", None]:
                        servicesList = servicesList.filter(price__lte=float(query.get("maxPrice")))

        servicesList = servicesList.values_list('id', flat=True)
        uniqueServiceList = set(list(servicesList))
        print uniqueServiceList
        services = Services.objects.filter(pk__in=set(list(servicesList)))

        if query.get("distance") not in ["", None] and  query.get("lat") not in ["", None] and query.get("lon") not in ["", None]:
            for service in services:
                # check location
                if service.location_constraint == True:
                    distance = utilities.getDistance(float(query.get("lat")), float(query.get("lon")), service.latitude, service.longitude) 
                    print distance                       

                    if 0 <= float(distance) <= float(query.get("distance")): 
                        # check QoS
                        rating = ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0]
                        reviews = ConsumersToServices.objects.filter(service_id=service.id).count()

                        if query.get("minQoS") != None and query.get("maxQoS") != None:
                            if int(reviews) > 0 and float(query.get("minQoS")) <= float(rating) <= float(query.get("maxQoS")):
                                pass
                            else:
                                uniqueServiceList.remove(service.id)
                    else:
                        uniqueServiceList.remove(service.id)
        else:
            for service in services:
                # check QoS
                rating = ConsumersToServices.objects.filter(service_id=service.id).aggregate(Avg('rating')).values()[0]
                reviews = ConsumersToServices.objects.filter(service_id=service.id).count()
                                
                if query.get("minQoS") != None and query.get("maxQoS") != None:
                    if int(reviews) > 0 and float(query.get("minQoS")) <= float(rating) <= float(query.get("maxQoS")):
                        print service.id, "OK"
                    else:
                        uniqueServiceList.remove(service.id)
        
        order_by = query.get("sortby") if "sortby" in query else "id"
        queryset = Services.objects.filter(pk__in=uniqueServiceList).order_by(order_by)
        return queryset

class SearchArticlesList(generics.ListAPIView):
    """
        Retrieve public articles in topic
        ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: topics
                description: Topics ID (comma delimiter)
                type: string
                paramType: query
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
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """

    serializer_class = ArticleSerializer

    def get_queryset(self):
        """Override method"""

        articles = Article.objects.all()

        if 'topics' in self.request.query_params:
            topics = self.request.query_params.get('topics', None)
            if topics not in [u'', None]:
                topicsList = list()
                for i in str(topics).split(','):
                    if i.isdigit():
                        topicsList.append(i)
                if  type(topicsList) is list and len(topicsList):
                    return articles.filter(topic_id__in=topicsList)
            return Article.objects.filter(topic_id__in=[])
        return articles

class CustomSearchEngine(MultipleModelAPIView):
    """
    Retrieve a list of services based on filters and a list of relevant help articles
    """
    objectify = True

    def get_queryList(self):
        """Override method"""

        servicesList = Services.objects.all()
        articlesList = Article.objects.all()

        # Filter services based on categories
        if 'categories' in self.request.query_params:
            categories = self.request.query_params.get('categories', None)
            categoriesList = list()
            if categories not in [u'', '', None]:
                for i in str(categories).split(','):
                    if i.isdigit():
                        categoriesList.append(i)
            if  type(categoriesList) is list and len(categoriesList):
                servicesList = servicesList.filter(categories__pk__in=categoriesList)

        # Find out where services provide the incoming type of technical support
        if 'technical_support' in self.request.query_params:
            technicalSupport = self.request.query_params.get('technical_support', None)
            technicalSupportList = list()
            if technicalSupport not in [u'', '', None]:
                for i in str(technicalSupport).split(','):
                    if i.isdigit():
                        technicalSupportList.append(i)
                if type(technicalSupportList) is list and len(technicalSupportList):
                    available = set(list(ServicesToTechnicalSupport.objects.\
                        filter(technical_support_id__in=technicalSupportList).values_list('service_id', flat=True)))
                    servicesList = servicesList.filter(pk__in=available)

        # Filter based on service IDs
        if 'services' in self.request.query_params:
            services = self.request.query_params.get('services', None)
            tempList = list()
            if services not in [u'', '', None]:
                for i in str(services).split(','):
                    if i.isdigit():
                        tempList.append(i)
                if type(tempList) is list and len(tempList):
                    servicesList = servicesList.filter(pk__in=tempList)

        if 'topics' in self.request.query_params:
            topics = self.request.query_params.get('topics', None)
            if topics not in [u'', None]:
                topicsList = list()
                for i in str(topics).split(','):
                    if i.isdigit():
                        topicsList.append(i)
                if  type(topicsList) is list and len(topicsList):
                    articlesList = articlesList.filter(topic_id__in=topicsList)
        
        servicesList = servicesList.values_list('id', flat=True)
        uniqueServiceList = set(list(servicesList))
        
        return [
            (Services.objects.filter(pk__in=uniqueServiceList),ServiceSerializer,'services'),
            (articlesList.filter(service_id__in=uniqueServiceList),ArticleSerializer,'articles')
        ]


class KeywordsEngine(generics.ListAPIView):
    """
        Retrieve services based on user keywords
        ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: q
                description: Keywords (delimeters ,;| and space)
                type: string
                paramType: query
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
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """

    serializer_class = ServiceSerializer

    def get_queryset(self):
        """Filter services based on user keywords"""

        # ignore terms with less than 3 characters
        user_input = self.request.GET.get('q', None)

        if user_input not in ["", None]:
          user_input = user_input.lower()
          keywords = re.split('[,;| ]+', user_input)
          keyword_list = [str(term) for term in keywords if len(term) > 2]

          services_list = list()
          for keyword in keyword_list:
              ids_list = Services.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword)).exclude(is_visible=False).values_list('id', flat=True)
              services_list += ids_list

          return Services.objects.filter(pk__in=services_list).distinct().order_by('title')

        else:
          return Services.objects.exclude(is_visible=False).order_by('title')


class CustomKeywordsEngine(MultipleModelAPIView):
    """
        Retrieve services based on user keywords
        ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: q
                description: Keywords (delimeters ,;| and space)
                type: string
                paramType: query
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
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json
            produces:
              - application/json
              - application/xml
    """

    objectify = True

    def get_queryList(self):
        """Filter services based on user keywords"""

        # ignore terms with less than 3 characters
        user_input = self.request.GET.get('q', None)

        if user_input not in ["", None]:
            user_input = user_input.lower()
            keywords = re.split('[,;| ]+', user_input)
            keyword_list = [str(term) for term in keywords if len(term) > 2]

            services_list = list()
            articles_list = list()
            for keyword in keyword_list:
                ids_list = Services.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword)).exclude(is_visible=False).values_list('id', flat=True)
                services_list += ids_list
                article_ids_list = Article.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).exclude(visible=False).values_list('id', flat=True)
                articles_list += article_ids_list

            return [
                (Services.objects.filter(pk__in=services_list).distinct().order_by('title'), ServiceSerializer,'services'),
                (Article.objects.filter(pk__in=articles_list).distinct().order_by('title'), ArticleSerializer,'articles')
            ]

        else:

            return [
                (Services.objects.exclude(is_visible=False).order_by('title'), ServiceSerializer,'services'),
                (Article.objects.exclude(visible=False).order_by('title'), ArticleSerializer,'articles')
            ]