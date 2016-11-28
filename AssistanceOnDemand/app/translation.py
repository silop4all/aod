# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext as _
from modeltranslation.translator import translator, TranslationOptions
from app.models import (
    Components,
    ItExperience,
    Tags,
    Categories,
    ChargingPolicies,
    Services,
    ServiceKeywords,
    ServiceConfiguration,
    TechnicalSupport,
    ServicesToTechnicalSupport,
    ConsumersToServices,
    NasConfiguration,
    Topic,
    Article,
    ArticleDocument,
    ArticleVideo,
    CookiePolicy,
)

REQUIRED_LANGUAGES = tuple([v[0] for i,v in enumerate(settings.LANGUAGES)])


class ComponentsTranslationOptions(TranslationOptions):
    fields = ('description',)
    required_languages = REQUIRED_LANGUAGES
translator.register(Components, ComponentsTranslationOptions)

class ItExperienceTranslationOptions(TranslationOptions):
    fields = ('level', 'description',)
    required_languages = REQUIRED_LANGUAGES
translator.register(ItExperience, ItExperienceTranslationOptions)

class TagsTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = REQUIRED_LANGUAGES
translator.register(Tags, TagsTranslationOptions)

class CategoriesTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
    required_languages = REQUIRED_LANGUAGES
translator.register(Categories, CategoriesTranslationOptions)

class ChargingPoliciesTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)
    required_languages = REQUIRED_LANGUAGES
translator.register(ChargingPolicies, ChargingPoliciesTranslationOptions)

class ServicesTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'requirements', 'installation_guide', 'usage_guidelines', 'constraints', )
    #group_fieldsets = True
    #fallback_values = {
    #    'installation_guide': _('-- installation guide has not translated --'),
    #    'constraints': _('-- constraints  have not translated--')
    #}
    #fallback_undefined = {
    #    'installation_guide': 'None installation guide is provided',
    #    'constraints': 'None',
    #}
    required_languages = REQUIRED_LANGUAGES
translator.register(Services, ServicesTranslationOptions)

class ServiceKeywordsTranslationOptions(TranslationOptions):
    fields = ('title', )
translator.register(ServiceKeywords, ServiceKeywordsTranslationOptions)

class ServiceConfigurationTranslationOptions(TranslationOptions):
    fields = ('parameter', 'value')
translator.register(ServiceConfiguration, ServiceConfigurationTranslationOptions)

class TechnicalSupportTranslationOptions(TranslationOptions):
    fields = ('type', 'description')
    required_languages = REQUIRED_LANGUAGES
translator.register(TechnicalSupport, TechnicalSupportTranslationOptions)

class ServicesToTechnicalSupportTranslationOptions(TranslationOptions):
    fields = ('title', 'software_dependencies')
translator.register(ServicesToTechnicalSupport, ServicesToTechnicalSupportTranslationOptions)

#class ConsumersToServicesTranslationOptions(TranslationOptions):
#    fields = ('rating_rationale',)
#translator.register(ConsumersToServices, ConsumersToServicesTranslationOptions)

class NasConfigurationTranslationOptions(TranslationOptions):
    fields = ('parameter', 'value')
translator.register(NasConfiguration, NasConfigurationTranslationOptions)

class AbstractBasicTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    
    class Meta:
        abstract = True

class TopicTranslationOptions(AbstractBasicTranslationOptions):
    fields = ('title', 'description')
translator.register(Topic, TopicTranslationOptions)

class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
translator.register(Article, ArticleTranslationOptions)

class ArticleDocumentTranslationOptions(AbstractBasicTranslationOptions):
    pass
translator.register(ArticleDocument, ArticleDocumentTranslationOptions)

class ArticleVideoTranslationOptions(AbstractBasicTranslationOptions):
    pass
translator.register(ArticleVideo, ArticleVideoTranslationOptions)

class CookiePolicyTranslationOptions(TranslationOptions):
    fields = ('content',)
translator.register(CookiePolicy, CookiePolicyTranslationOptions)