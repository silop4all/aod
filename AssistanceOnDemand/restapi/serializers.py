from rest_framework import serializers
from app.models import *


class ItExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItExperience
        fields = ('id', 'level', 'description')


class UserSerializer(serializers.ModelSerializer):
    experience = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Users
        fields = ('name', 'lastname', 'username', 'pwd', 'email', 'mobile', 'country', 'experience')


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'name', 'lastname', 'username', 'email', )
        depth = 2



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'category', 'question', 'children', 'tags')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'category', 'question', 'children', 'tags')
        depth = 1

class TreeCategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    children = SubCategorySerializer(read_only=True, many=True)
    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'category', 'question', 'children', 'tags')
        depth = 1


class ChargingPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingPolicies
        fields = ('id', 'name', 'description')


class ServiceLanguagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceLanguages
        fields = '__all__'


class ServiceKeywordsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceKeywords
        fields = '__all__'


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceConfiguration
        #fields = '__all__'
        fields   =  ('id', 'parameter', 'value',)

class TechnicalSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSupport
        fields = '__all__'

class ServiceTechnicalSupportSerializer(serializers.ModelSerializer):
    technical_support_type = TechnicalSupportSerializer(read_only=True, many=True)
    class Meta:
        model = ServicesToTechnicalSupport
        fields = ('id', 'title', 'service','technical_support','path', 'software_dependencies',
            'format', 'technical_support_type', 'created_date', 'modified_date', 'visible'
        )
        depth=1

class ServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'categories', 'type', 'charging_policy', 'owner', 
            'price', 'unit', 'version', 'license','requirements', 'installation_guide', 
            'usage_guidelines', 'is_public', 'constraints', 'coverage', 'skype',
            'language_constraint', 'location_constraint', 'latitude', 'longitude',  
            'created_date', 'modified_date',
            'languages', 'keywords', 'configuration', 'technical_support'
        )

class DetailedServiceSerializer(serializers.ModelSerializer):
    categories      = CategorySerializer(read_only=True, many=True)
    #type            = ChoicesField(choices=Services.MY_CHOICES)
    charging_policy = ChargingPolicySerializer(read_only=True, many=False)
    languages       = ServiceLanguagesSerializer(read_only=True, many=True)
    keywords        = ServiceKeywordsSerializer(read_only=True, many=True)
    configuration   = ConfigurationSerializer(read_only=True, many=True)
    technical_support = ServiceTechnicalSupportSerializer(read_only=True, many=True)
    
    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'categories', 'type', 'charging_policy', 'owner', 
            'price', 'unit', 'version', 'license','requirements', 'installation_guide', 
            'usage_guidelines', 'is_public', 'constraints', 
            'language_constraint', 'location_constraint', 'latitude', 'longitude',  
            'created_date', 'modified_date', 'image', 'coverage', 'skype',
            'languages', 'keywords', 'configuration', 'technical_support',
        )
        depth = 1

class ServiceConfigurationsSerializer(serializers.ModelSerializer):
    configuration   = ConfigurationSerializer(read_only=True, many=True)
    
    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'configuration')

class ServiceLanguagesSerializer(serializers.ModelSerializer):
    languages       = ServiceLanguagesSerializer(read_only=True, many=True)
    
    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'languages')

class ServiceTechicalSupportSerializer(serializers.ModelSerializer):
    technical_support = ServiceTechnicalSupportSerializer(read_only=True, many=True)
    
    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'skype', 'technical_support')

class ServiceKeywordsSerializer(serializers.ModelSerializer):
    keywords        = ServiceKeywordsSerializer(read_only=True, many=True)
    
    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'keywords',)


class ServiceReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumersToServices
        fields = ('id', 'consumer', 'rating', 'rating_rationale', 'purchased_date', )
        depth = 2


class ConsumerServicesSerializer(serializers.ModelSerializer):
    """Fetch services information that a consumer has purchased"""
    service = ServiceSerializer(read_only=True, many=False)
    class Meta:
        model = ConsumersToServices
        fields = ('pk', 'service',)
        depth = 1




# Assistance serializers
class ConsumerAssistServicesSerializer(serializers.ModelSerializer):
    """Services information that carers have purchased on behalf a consumer"""
    service = ServiceSerializer(read_only=True, many=False)
    class Meta:
        model = NasConsumersToServices
        fields = ('pk', 'service', )
        depth = 1

class AssistanceConfigurationSerializer(serializers.ModelSerializer):
    """Configuration per service that a carer has purchased"""
    class Meta:
        model = NasConfiguration
        fields   =  ('id', 'nas', 'parameter', 'value', 'is_default')

class ConsumerAssistServicesConfigurationSerializer(serializers.ModelSerializer):
    """Configuration per service that consumer has purchased via  a carer"""
    configuration = AssistanceConfigurationSerializer(read_only=True, many=True)

    class Meta:
        model = NasConsumersToServices
        fields = ('id', 'configuration', ) 
        depth = 1



class UserThemeSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = UserTheme
        fields = '__all__'


class PublishQuestionSerializer(serializers.ModelSerializer):
    """Serialize the incoming questions"""
    class Meta:
        model = IncomingQuestions
        fields = '__all__'




class SimpleServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Services
        fields = '__all__'