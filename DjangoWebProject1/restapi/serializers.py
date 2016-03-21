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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'category', 'question', 'children',)
        #depth = 3


class ChargingPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingPolicies
        fields = ('id', 'name', 'description')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('id', 'title', 'description', 'categories', 'type', 'charging_policy', 'owner', 
            'price', 'unit', 'version', 'license','requirements', 'installation_guide', 
            'link', 'usage_guidelines', 'availability', 'constraints',
            'language_constraint', 'location_constraint', 'latitude', 'longitude',  
            'created_date', 'modified_date'
        )

class ServiceConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceConfiguration
        fields = '__all__'


class CarerAssistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarersAssistConsumers
        
        fields = ('carer', 'consumer', 'response', 'state', 'created_at', 'updated_at')
        depth = 1

