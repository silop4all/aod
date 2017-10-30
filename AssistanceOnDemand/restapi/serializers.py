
from django.conf import settings
from rest_framework import serializers
from app.models import *
from django.db.models import (
    Avg,
    Sum,
    Q
)


class ItExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItExperience
        fields = ('id', 'level', 'description')


class UserSerializer(serializers.ModelSerializer):
    experience = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Users
        fields = ('name', 'lastname', 'username', 'pwd',
                  'email', 'mobile', 'country', 'experience')


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'name', 'lastname', 'username', 'email', )
        depth = 2


class CarerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('name', 'lastname', 'username', 'email', 'mobile')
        # depth = 2     


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'category',
                  'question', 'children', 'tags')


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'category',
                  'question', 'children', 'tags')
        depth = 1


class TreeCategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    children = SubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'category',
                  'question', 'children', 'tags')
        depth = 1


class ChargingPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = ChargingPolicies
        fields = ('id', 'name', 'description')


class ServiceLanguagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceLanguages
        fields = '__all__'


class ServiceLanguagesListSerializer(serializers.ModelSerializer):
    languages = ServiceLanguagesSerializer(read_only=True, many=True)

    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'languages')


class ServiceKeywordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceKeywords
        fields = '__all__'


class ServiceKeywordsListSerializer(serializers.ModelSerializer):
    keywords = ServiceKeywordsSerializer(read_only=True, many=True)

    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'keywords',)


class ConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceConfiguration
        #fields = '__all__'
        fields = ('id', 'parameter', 'value',)


class TechnicalSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalSupport
        fields = '__all__'


class SimpleServiceTechnicalSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServicesToTechnicalSupport
        fields = ('id', 'title', 'service', 'technical_support', 'path', 'link',
                  'description', 'software_dependencies', 'extension', 'visible',
                  'created_date', 'modified_date',
                  )


class ServiceTechnicalSupportSerializer(serializers.ModelSerializer):
    technical_support_type = TechnicalSupportSerializer(
        read_only=True, many=True)

    class Meta:
        model = ServicesToTechnicalSupport
        fields = ('id', 'title', 'service', 'technical_support', 'path', 'link',
                  'description', 'software_dependencies', 'extension', 'visible',
                  'technical_support_type', 'created_date', 'modified_date',
                  )
        depth = 1


class ServiceConsumerSerializer(serializers.ModelSerializer):
    """Fetch the consumers of service as well as consumer rating and review"""

    class Meta:
        model = ConsumersToServices
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    """
    Fetch the major fields of service as well as a few derived ones (relationships) such as:
    - Service consumers object: JSON
    - Number of consumers' reviews per service: None or integer
    - Average value of consumers' ratings per service: None or Float
    """

    service_consumers = ServiceConsumerSerializer(many=True, read_only=True)
    total_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    image_path = serializers.SerializerMethodField()
    owner_logo = serializers.SerializerMethodField()

    def get_total_reviews(self, obj):
        """Count the number of consumer reviews per service"""
        return obj.reviews_count

    def get_average_rating(self, obj):
        """Fetch the average rating of consumer reviews per service"""
        return obj.review_score

    def get_image_path(self, obj):
        """Fix the URL of image"""
        try:
            image = Services.objects.get(pk=obj.id).image
            if image not in ['', None]:
                return image.url.replace(settings.MEDIA_URL, settings.MEDIA_URL + 'app/services/images/')
            return None
        except:
            return None

    def get_owner_logo(self, obj):
        """Get the logo of service owner if any"""
        user_logo = obj.owner.user.logo
        if user_logo not in ["", None]:
            return settings.MEDIA_URL + "app/users/logos/" + str(user_logo)
        else:
            return ""

    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'categories', 'type', 'charging_policy', 'owner',
                  'price', 'unit', 'version', 'license', 'requirements', 'installation_guide',
                  'usage_guidelines', 'is_public', 'constraints', 'coverage', 'skype',
                  'language_constraint', 'location_constraint', 'latitude', 'longitude',
                  'created_date', 'modified_date', 'image_path', 'image',
                  'languages', 'keywords', 'configuration', 'technical_support',
                  'service_consumers', 'total_reviews', 'average_rating', 'owner_logo',
                  )


class SimpleServiceSerializer(serializers.ModelSerializer):
    """Fetch all fields of service"""
    class Meta:
        model = Services
        fields = '__all__'


class ServiceConfigurationsSerializer(serializers.ModelSerializer):
    configuration = ConfigurationSerializer(read_only=True, many=True)

    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'configuration')


class ServiceTechicalSupportSerializer(serializers.ModelSerializer):
    technical_support = ServiceTechnicalSupportSerializer(
        read_only=True, many=True)

    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'skype', 'technical_support')


class ServiceReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumersToServices
        fields = ('id', 'consumer', 'rating', 'rating_rationale', 'purchased_date',
                  'advantages', 'disadvantages', 'review_date')
        depth = 2


class ConsumerServicesSerializer(serializers.ModelSerializer):
    """Fetch services information that a consumer has purchased"""
    service = ServiceSerializer(read_only=True, many=False)

    class Meta:
        model = ConsumersToServices
        fields = ('pk', 'service',)
        depth = 1


class DetailedServiceSerializer(serializers.ModelSerializer):
    """Fetch the fields of services and the ones of the relevant models"""

    image_path = serializers.SerializerMethodField()
    categories = CategorySerializer(read_only=True, many=True)
    #type            = ChoicesField(choices=Services.MY_CHOICES)
    charging_policy = ChargingPolicySerializer(read_only=True, many=False)
    languages = ServiceLanguagesSerializer(read_only=True, many=True)
    keywords = ServiceKeywordsSerializer(read_only=True, many=True)
    configuration = ConfigurationSerializer(read_only=True, many=True)
    technical_support = ServiceTechnicalSupportSerializer(
        read_only=True, many=True)
    reviews = ServiceReviewsSerializer(read_only=True, many=True)

    def get_image_path(self, obj):
        """Fix the URL of image"""
        try:
            image = Services.objects.get(pk=obj.id).image
            if image not in ['', None]:
                return image.url.replace(settings.MEDIA_URL, settings.MEDIA_URL + 'app/services/images/')
            return None
        except:
            return None

    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'categories', 'type', 'charging_policy', 'owner',
                  'price', 'unit', 'version', 'license', 'requirements', 'installation_guide',
                  'usage_guidelines', 'is_public', 'constraints',
                  'language_constraint', 'location_constraint', 'latitude', 'longitude',
                  'created_date', 'modified_date', 'image', 'image_path', 'coverage', 'skype',
                  'languages', 'keywords', 'configuration', 'technical_support', 'reviews'
                  )
        depth = 1


class ConsumerAssistServicesSerializer(serializers.ModelSerializer):
    """Services information that carers have purchased on behalf a consumer"""
    service = ServiceSerializer(read_only=True, many=False)

    class Meta:
        model = ConsumersToServices
        fields = ('pk', 'service', )
        depth = 1


class AssistanceConfigurationSerializer(serializers.ModelSerializer):
    """Configuration per service that a carer has purchased"""
    class Meta:
        model = NasConfiguration
        fields = ('id', 'nas', 'parameter', 'value', 'is_default')


class ConsumerAssistServicesConfigurationSerializer(serializers.ModelSerializer):
    """Configuration per service that consumer has purchased via  a carer"""
    configuration = AssistanceConfigurationSerializer(
        read_only=True, many=True)

    class Meta:
        model = ConsumersToServices
        fields = ('id', 'configuration', )
        depth = 1


class UserThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTheme
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serialize the FAQ articles
    """
    class Meta:
        model = Article
        fields = '__all__'


class PublishQuestionSerializer(serializers.ModelSerializer):
    """Serialize the incoming questions"""
    class Meta:
        model = IncomingQuestions
        fields = '__all__'


class CarerSerializer(serializers.ModelSerializer):
    """Serialize the part of the carer's profile
    """
    user = CarerProfileSerializer(read_only=True, many=False)

    class Meta:
        model = Carers
        fields = ('user', )
