from django.contrib import admin
from app.models import *
from import_export.admin import ImportExportModelAdmin


class ComponentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_enabled']
    ordering = ['name',]
    list_filter = ['is_enabled',]
admin.site.register(Components, ComponentsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title', 'category', 'description', 'question')
    ordering = ['category','title']
    fields = (('title', 'description'), 'category', 'question', 'tags')
    list_filter = ['category__title', 'tags__title']
    search_fields = ['title', 'description']
    list_per_page = 20
admin.site.register(Categories, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    ordering = ['title']
    search_fields = ['title']
admin.site.register(Tags, TagAdmin)


class ItExperienceAdmin(admin.ModelAdmin):
    list_display = ['level', 'description']
    ordering = ['level']
    fields = ['level', 'description']
    search_fields = ['level']
    list_filter = ['level']
admin.site.register(ItExperience, ItExperienceAdmin)

class ChargingPoliciesAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    fields = ['name', 'description']
admin.site.register(ChargingPolicies, ChargingPoliciesAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'lastname', 'gender', 'email', 'country', 'it_experience', 'is_active', 'registration']
    fields = [('gender','name', 'lastname'), 'username', ('email', 'mobile'), ('country', 'city'), ('address', 'postal_code'), ('logo', 'cover'), 'categories', ('registration', 'last_login'), 'is_active']
    #exclude = ['pwd']
    ordering = ['username', 'name', 'lastname']
    list_filter = ['country', 'city', 'is_active', 'gender', 'experience__level']
    search_fields = ['name', 'lastname', 'username', 'email', ]
    list_display_links = ['username']
    list_per_page = 20
    date_hierarchy  = 'registration'
    actions_on_bottom = True

    def it_experience(self, obj):
        return obj.experience.level
admin.site.register(Users, UserAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', '_category', 'type', 'charging_policy', 'price', 'is_available', 'location_constraint', 'language_constraint', 'created_date']
    fields = ['title', 'description', 'categories', 'type', 'charging_policy',  ('image', 'cover'), ('version', 'license'), ('price', 'unit'), 'requirements', 
        'installation_guide', ('software', 'link'), 'usage_guidelines', 'constraints', ('availability', 'is_available'), ('location_constraint', 'latitude', 'longitude'), 
        'language_constraint', ('created_date', 'modified_date'),
    ]
    ordering = ['categories__title', 'type', 'charging_policy__name']
    list_filter = ['categories', 'type', 'charging_policy', 'price', 'is_available', 'location_constraint', 'language_constraint']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_date'
    list_per_page = 10

    def charging_policy(self, obj):
        return obj.charging_policy.name

    def _category(self, object):
        return "\n".join([str(p) for p in object.categories.all()])

admin.site.register(Services, ServiceAdmin)


class ServiceKeywordAdmin(admin.ModelAdmin):
    list_display = ['service', 'title']
    list_filter = ['service__title', 'title']
    #search_fields = ['service']
    ordering = ['title']
admin.site.register(ServiceKeywords, ServiceKeywordAdmin)


class ServiceLanguagesAdmin(admin.ModelAdmin):
    list_display = ['service', 'alias']
    list_filter = ['service__title', 'alias']
    search_fields = ['alias']
    ordering = ['service', 'alias']
admin.site.register(ServiceLanguages, ServiceLanguagesAdmin)


class ServiceConfigurationAdmin(admin.ModelAdmin):
    list_display = ['service', 'parameter', 'value', 'is_default']
    list_filter = ['service__title', 'is_default']
    fields = ['service', ('parameter', 'value'), 'is_default']
    ordering = ['service', 'parameter', 'value']
admin.site.register(ServiceConfiguration, ServiceConfigurationAdmin)



#admin.site.register(UserRole)

class ProviderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'crowd_fund_participation', 'crowd_fund_notification']
    ordering = ['user']
    search_fields = ['user']
    list_filter = ['is_active', 'crowd_fund_participation', 'crowd_fund_notification']
    list_display_links = []
admin.site.register(Providers, ProviderAdmin)


class ConsumersAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'crowd_fund_participation', 'crowd_fund_notification']
    ordering = ['user']
    search_fields = ['user']
    list_filter = ['is_active', 'crowd_fund_participation', 'crowd_fund_notification']
    list_display_links = []
admin.site.register(Consumers, ConsumersAdmin)


class CarerAdmin(admin.ModelAdmin):
    list_display = ['_carer', 'is_active']
    #fields = ['user', 'is_active']
    ordering = ['user']
    #search_fields = ['user']
    list_filter = ['is_active']
    list_display_links = []

    def _carer(self, obj):
        return (" %s %s") % (obj.user.name, obj.user.lastname)
admin.site.register(Carers, CarerAdmin)


class CarersAssistConsumersAdmin(admin.ModelAdmin):
    list_display    = ['id', '_carer', '_consumer', 'response', 'state', 'created_at', 'updated_at']    
    list_filter     = ['response', 'state']
    search_fields   = ['created_at']
    date_hierarchy  = 'updated_at'
    list_per_page = 20

    def _carer(self, obj):
        return (" %s %s") % (obj.carer.user.name, obj.carer.user.lastname)

    def _consumer(self, obj):
        return (" %s %s") % (obj.consumer.user.name, obj.consumer.user.lastname)
admin.site.register(CarersAssistConsumers, CarersAssistConsumersAdmin)


class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    fields = ['type', 'description']
    ordering = ['type',]
admin.site.register(TechnicalSupport, TechnicalSupportAdmin)


class ServicesToTechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ['service', 'technical_support', 'path',]
    fields = ['service', 'technical_support', 'path', 'software_dependencies']  
    list_filter = ['service__title', 'technical_support__type']
    ordering = ['service', 'technical_support']
admin.site.register(ServicesToTechnicalSupport, ServicesToTechnicalSupportAdmin)


class ConsumersToServicesAdmin(admin.ModelAdmin):
    fields          = ['service', 'cost', 'purchased_date', 'rating', 'is_completed']
    list_display    = ['id', '_consumer', 'service', 'purchased_date', 'rating', 'is_completed']
    ordering        = ['consumer']
    list_per_page   = 20
    date_hierarchy  = 'purchased_date'
    list_filter     = ['rating', 'is_completed']

    def _consumer(self, obj):
        return (" %s %s") % (obj.consumer.user.name, obj.consumer.user.lastname)
admin.site.register(ConsumersToServices, ConsumersToServicesAdmin)


class NasConsumersToServicesAdmin(admin.ModelAdmin):
    fields          = ['service', 'cost', 'purchased_date', 'rating', 'is_completed']
    list_display    = ['id', '_consumer', 'service', 'purchased_date', 'rating', 'is_completed']
    ordering        = ['consumer']
    list_per_page   = 20
    date_hierarchy  = 'purchased_date'
    list_filter     = ['rating', 'is_completed']

    def _consumer(self, obj):
        return (" %s %s") % (obj.consumer.user.name, obj.consumer.user.lastname)
admin.site.register(NasConsumersToServices, NasConsumersToServicesAdmin)


class NasConfigurationAdmin(admin.ModelAdmin):
    fields          = ['id', 'nas', 'parameter', 'value', 'is_default']
    list_display    = ['_service', 'parameter', 'value', 'is_default']
    ordering        = ['nas']
    list_per_page   = 20
    list_filter     = ['nas__service__title', 'is_default']

    def _service(self, obj):
        return obj.nas.service.title

admin.site.register(NasConfiguration, NasConfigurationAdmin)


