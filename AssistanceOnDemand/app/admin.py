# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.db.models import *
from django.core.urlresolvers import reverse
from django.contrib.admin.models import LogEntry
from django.utils.translation import ugettext as _

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from ckeditor.widgets import CKEditorWidget

from app.models import (
    Components,
    Categories,
    Tags,
    ItExperience,
    ChargingPolicies,
    Users,
    Services,
    ServiceKeywords,
    ServiceLanguages,
    ServiceConfiguration,
    Providers,
    Consumers,
    Carers,
    CarersAssistConsumers,
    TechnicalSupport,
    ServicesToTechnicalSupport,
    ConsumersToServices,
    NasConfiguration,
    Tokens,
    Topic,
    Article,
    ArticleDocument,
    ArticleVideo,
    Logo,
    Favicon,
    SocialNetwork,
    LanguageFlag,
    Theme,
    UserTheme,
    Metadata,
    ContactUs,
    CookiePolicy,
    PlatformCommunityMember,
    EvaluationMetric,
    TermsUsage,
)
from app.utilities import sendEmail


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'content_type_id', 'action_time']
    ordering = ['action_time', 'user_id', ]
    list_filter = ['user_id__username', 'content_type_id', 'action_time', ]
admin.site.register(LogEntry, LogEntryAdmin)


class LogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'logo', 'mime_type',
                    'absolute_path', 'logo_size', 'logo_dimensions', 'selected']
    list_filter = ['selected', ]
    ordering = ['id', ]

    def mime_type(self, object):
        return object.logo.mimetype[0]

    def absolute_path(self, object):
        return object.logo.path_full

    def logo_size(self, object):
        return str(object.logo.filesize / 1024) + " KB"

    def logo_dimensions(self, object):
        return (" %s %s %s") % (str(object.logo.dimensions[0]), "x", str(object.logo.dimensions[1]))

    def save_model(self, request, object, form, change):
        existSelectedLogo = Logo.objects.filter(selected=True).count()
        if object.selected:
            Logo.objects.filter(selected=True).update(selected=False)
            messages.add_message(request, messages.INFO,
                                 'Logo ' + object.title + ' has been selected')
        if not existSelectedLogo:
            object.selected = True
        object.save()
admin.site.register(Logo, LogoAdmin)


class FaviconAdmin(admin.ModelAdmin):
    pass
    list_display = ['id', 'title', 'favicon', 'mime_type',
                    'absolute_path', 'favicon_size', 'favicon_dimensions', 'selected']
    list_filter = ['selected', ]
    ordering = ['id', ]

    def mime_type(self, object):
        return object.favicon.mimetype[0]

    def absolute_path(self, object):
        return object.favicon.path_full

    def favicon_size(self, object):
        return str(object.favicon.filesize / 1024) + " KB"

    def favicon_dimensions(self, object):
        return (" %s %s %s") % (str(object.favicon.dimensions[0]), "x", str(object.favicon.dimensions[1]))

    def save_model(self, request, object, form, change):
        existSelectedLogo = Favicon.objects.filter(selected=True).count()
        if object.selected:
            Favicon.objects.filter(selected=True).update(selected=False)
            messages.add_message(
                request, messages.INFO, 'Favicon ' + object.title + ' has been selected')
        if not existSelectedLogo:
            object.selected = True
        object.save()
admin.site.register(Favicon, FaviconAdmin)


class MetadataAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'keywords', 'author', 'active']
    list_filter = ['active', ]

    def save_model(self, request, object, form, change):
        metadataExistance = Metadata.objects.filter(active=True).count()
        if object.active:
            Metadata.objects.filter(active=True).update(active=False)
            messages.add_message(
                request, messages.INFO, 'Meta elements for the application has been selected')
        if not metadataExistance:
            object.active = True
        object.save()
admin.site.register(Metadata, MetadataAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'skype_id', 'skype_button_id',
                    'phone', 'email', 'address', 'active']
    list_filter = ['active', ]

    def save_model(self, request, object, form, change):
        activeContactDetails = ContactUs.objects.filter(active=True).count()
        if object.active:
            ContactUs.objects.filter(active=True).update(active=False)
            messages.add_message(
                request, messages.INFO, 'Contact details for the application has been inserted')
        if not activeContactDetails:
            object.active = True
        object.save()
admin.site.register(ContactUs, ContactUsAdmin)


class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'visible']
    list_filter = ['visible', ]
admin.site.register(SocialNetwork, SocialNetworkAdmin)


class ComponentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_enabled']
    fields = [('name', 'is_enabled'), 'description']
    ordering = ['id', 'name', ]
    list_filter = ['is_enabled', ]
admin.site.register(Components, ComponentsAdmin)


class LanguageFlagAdmin(admin.ModelAdmin):
    list_display = ['alias', 'flag', 'mime_type',
                    'absolute_path', 'flag_size', 'flag_dimensions']
    ordering = ['alias']

    def mime_type(self, object):
        return object.flag.mimetype[0]

    def absolute_path(self, object):
        return object.flag.path_full

    def flag_size(self, object):
        return str(object.flag.filesize) + " B"

    def flag_dimensions(self, object):
        return (" %s %s %s") % (str(object.flag.dimensions[0]), "x", str(object.flag.dimensions[1]))
admin.site.register(LanguageFlag, LanguageFlagAdmin)


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'category', 'description', 'question')
    ordering = ['category', 'id', 'title']
    fields = (('title', 'description'), 'category', 'question', 'tags')
    list_filter = ['category__title', 'tags__title']
    search_fields = ['title', 'description']
    list_per_page = 20
admin.site.register(Categories, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    ordering = ['title']
    search_fields = ['title']
    list_per_page = 20
admin.site.register(Tags, TagAdmin)


class ItExperienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'description']
    ordering = ['id']
    fields = ['level', 'description']
    search_fields = ['level']
    list_filter = ['level']
admin.site.register(ItExperience, ItExperienceAdmin)


class ChargingPoliciesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    ordering = ['id']
    fields = ['name', 'description']
admin.site.register(ChargingPolicies, ChargingPoliciesAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'name', 'lastname', 'gender',
                    'email', 'country', 'it_experience', 'is_active', 'registration']
    fields = ['username', ('name', 'lastname', 'gender'), ('email', 'mobile'), ('country', 'city'),
              ('address', 'postal_code'), ('logo', 'cover'), 'categories', ('registration', 'last_login'), 'is_active']
    readonly_fields = ['username', 'registration',
                       'last_login', 'email', 'mobile']
    ordering = ['username', 'name', 'lastname']
    list_filter = ['country', 'city', 'is_active', 'gender',
                   'experience__level', 'registration', 'last_login']
    search_fields = ['name', 'lastname', 'username', 'email', ]
    list_display_links = ['username']
    list_per_page = 10
    date_hierarchy = 'registration'
    actions_on_bottom = True

    def it_experience(self, obj):
        return obj.experience.level

    def has_add_permission(self, request):
        return False
admin.site.register(Users, UserAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', '_category', 'type', 'charging_policy', 'price',
                    'is_visible', 'location_constraint', 'language_constraint']
    fields = [('title', 'description'), ('image', 'is_public', 'is_visible'),
              ('type', 'categories'), ('charging_policy',
                                       'price', 'unit'), ('version', 'license'),
              'owner', ('requirements', 'installation_guide',
                        'usage_guidelines'),
              ('location_constraint', 'latitude', 'longitude', 'coverage'),
              'language_constraint', 'skype', ('created_date', 'modified_date')
              ]
    readonly_fields = ['categories', 'created_date', 'modified_date',
                       'type', 'price', 'unit', 'charging_policy', 'owner']
    ordering = ['id', 'type', 'charging_policy__name']
    list_filter = ['categories', 'type', 'charging_policy', 'price', 'owner', 'is_visible',
                   'location_constraint', 'language_constraint', 'created_date', 'modified_date']
    search_fields = ['title', 'description']
    #date_hierarchy  = 'created_date'
    list_per_page = 10

    def charging_policy(self, obj):
        return obj.charging_policy.name

    def _category(self, object):
        return ",".join([str(p) for p in object.categories.all()])

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ServiceAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Services, ServiceAdmin)


class ServiceKeywordAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'service', ]
    fields = ['title', 'service', ]
    readonly_fields = ['service']
    list_filter = ['service__title', 'title']
    ordering = ['title']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ServiceKeywords, ServiceKeywordAdmin)


class ServiceLanguagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'alias']
    list_filter = ['service__title', 'alias']
    fields = ['alias', 'service']
    readonly_fields = ['service']
    search_fields = ['alias']
    ordering = ['service', 'alias']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ServiceLanguages, ServiceLanguagesAdmin)


class ServiceConfigurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'parameter', 'value', 'is_default']
    list_filter = ['service__title', 'is_default']
    fields = ['service', ('parameter', 'value'), 'is_default']
    ordering = ['service', 'parameter', 'value']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ServiceConfiguration, ServiceConfigurationAdmin)


class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_active',
                    'crowd_fund_participation', 'crowd_fund_notification']
    fields = ['user', ('is_active'), ('crowd_fund_participation',
                                      'crowd_fund_notification'), 'company']
    readonly_fields = ['user', 'company']
    ordering = ['user']
    search_fields = ['user__username', 'user__name', 'user__lastname', ]
    list_filter = ['is_active', 'crowd_fund_participation',
                   'crowd_fund_notification', 'company']
    list_display_links = []

    def has_add_permission(self, request):
        return False
admin.site.register(Providers, ProviderAdmin)


class ConsumersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_active',
                    'crowd_fund_participation', 'crowd_fund_notification']
    fields = ['user', ('is_active'),
              ('crowd_fund_participation', 'crowd_fund_notification')]
    readonly_fields = ['user', ]
    ordering = ['user']
    search_fields = ['user__username', 'user__name', 'user__lastname']
    list_filter = ['is_active', 'crowd_fund_participation',
                   'crowd_fund_notification']
    list_display_links = []

    def has_add_permission(self, request):
        return False
admin.site.register(Consumers, ConsumersAdmin)


class CarerAdmin(admin.ModelAdmin):
    list_display = ['id', 'view_carer_info', 'is_active']
    readonly_fields = ['user', ]
    fields = [('user', 'is_active')]
    ordering = ['user']
    search_fields = ['user__username', 'user__name', 'user__lastname']
    list_filter = ['is_active']
    list_display_links = []

    def view_carer_info(self, obj):
        return (" %s %s") % (obj.user.name, obj.user.lastname)

    def has_add_permission(self, request):
        return False
admin.site.register(Carers, CarerAdmin)


class CarersAssistConsumersAdmin(admin.ModelAdmin):
    list_display = ['id', '_carer', '_consumer', 'response', 'state']
    list_filter = ['response', 'state', 'created_at', 'updated_at']
    fields = ['carer', 'consumer', 'response',
              'state', 'created_at', 'updated_at']
    readonly_fields = ['carer', 'consumer', 'created_at', 'updated_at']
    search_fields = ['created_at']
    date_hierarchy = 'updated_at'
    list_per_page = 20

    def _carer(self, obj):
        return (" %s %s") % (obj.carer.user.name, obj.carer.user.lastname)

    def _consumer(self, obj):
        return (" %s %s") % (obj.consumer.user.name, obj.consumer.user.lastname)

    def has_add_permission(self, request):
        return False
admin.site.register(CarersAssistConsumers, CarersAssistConsumersAdmin)


class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'description']
    fields = ['type', 'description']
    ordering = ['id', ]
admin.site.register(TechnicalSupport, TechnicalSupportAdmin)


class ServicesToTechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'service',
                    'technical_support', 'path', 'extension', ]
    fields = ['service', 'description', 'technical_support',
              'path', 'software_dependencies']
    list_filter = ['service__title', 'technical_support__type']
    ordering = ['service', 'technical_support']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ServicesToTechnicalSupport,
                    ServicesToTechnicalSupportAdmin)


class ConsumersToServicesAdmin(admin.ModelAdmin):
    fields = ['service', 'cost', 'purchased_date', 'rating', 'is_completed']
    readonly_fields = fields
    list_display = ['id', '_consumer', 'service',
                    'purchased_date', 'rating', 'is_completed']
    ordering = ['consumer']
    list_per_page = 20
    date_hierarchy = 'purchased_date'
    list_filter = ['rating', 'is_completed']

    def _consumer(self, obj):
        return (" %s %s") % (obj.consumer.user.name, obj.consumer.user.lastname)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ConsumersToServices, ConsumersToServicesAdmin)


class NasConfigurationAdmin(admin.ModelAdmin):
    fields = ['id', 'nas', 'parameter', 'value', 'is_default']
    list_display = ['id', '_service', 'parameter', 'value', 'is_default']
    ordering = ['nas']
    list_per_page = 20
    list_filter = ['nas__service__title', 'is_default']

    def _service(self, obj):
        return obj.nas.service.title
admin.site.register(NasConfiguration, NasConfigurationAdmin)


class TokensAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',  'access_token', 'refresh_token', 'scope']
    fields = ['user', 'access_token', 'refresh_token',
              'expires_in', 'scope', 'token_type']
    readonly_fields = fields
    search_fields = ['access_token', 'refresh_token', ]
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(TokensAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
admin.site.register(Tokens, TokensAdmin)


class ArticleInline(admin.StackedInline):
    model = Article


class ArticleVideoInline(admin.StackedInline):
    model = ArticleVideo


class ArticleDocumentInline(admin.StackedInline):
    model = ArticleDocument


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'included_articles',
                    'created_date', 'modified_date', 'visible', 'protected']
    list_filter = ['title', 'created_date',
                   'modified_date', 'visible', 'protected']
    ordering = ['id']
    search_fields = ['title', 'description', ]
    #date_hierarchy  = 'created_date'
    list_per_page = 20
    # inlines = [
    #    ArticleInline,
    #]

    def included_articles(self, object):
        return object.articles.count()
admin.site.register(Topic, TopicAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'topic', 'included_videos', 'included_documents',
                    'service', 'published_date', 'modified_date', 'visible', 'protected']
    list_filter = ['title', 'topic', 'published_date',
                   'modified_date', 'visible', 'protected', 'service']
    ordering = ['topic', 'id']
    search_fields = ['title', 'content']
    #date_hierarchy  = 'published_date'
    list_per_page = 20
    # inlines = [
    #    ArticleVideoInline,
    #    ArticleDocumentInline
    #]

    def included_videos(self, object):
        return object.videos.count()

    def included_documents(self, object):
        return object.docs.count()
admin.site.register(Article, ArticleAdmin)


class AbstractArticleEntityAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'article_title', 'element',
                    'extension', 'published_date', 'visible', 'protected']
    list_filter = ['published_date', 'article', 'visible', 'protected']
    search_fields = ['title', 'description', ]
    #date_hierarchy  = 'published_date'
    list_per_page = 20

    def article_title(self, object):
        return object.article.title

    def extension(self, object):
        return object.element.extension.replace('.', '').upper()

    # def link_to_article(self, object):
    #    link     = reverse('admin:app_article_change', args=(object.article.id))
    #    return u'<a href="%s">%s</a>' % (link, object.article.title)
    #    #return u'<a href="/el/admin/app/article/">aaa</a>'
    #link_to_article.allow_tags = True

    class Meta:
        abstract = True


class ArticleDocumentAdmin(AbstractArticleEntityAdmin):
    pass
admin.site.register(ArticleDocument, ArticleDocumentAdmin)


class ArticleVideoAdmin(AbstractArticleEntityAdmin):
    pass
admin.site.register(ArticleVideo, ArticleVideoAdmin)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'success_base', 'primary_base', 'info_base',
                    'warning_base', 'danger_base', 'radius', 'is_visible', 'is_default']
    fields = [('title', 'is_visible', 'is_default'), 'url', 'success_base',
              'primary_base', 'info_base', 'warning_base', 'danger_base', 'radius']
    list_filter = ['radius', 'is_visible', 'is_default']
    search_fields = ['title', 'url', ]
    list_per_page = 10

    def save_model(self, request, object, form, change):
        defaultTheme = Theme.objects.filter(is_default=True).count()
        if object.is_default:
            Theme.objects.filter(is_default=True).update(is_default=False)
            messages.add_message(
                request, messages.SUCCESS, 'The default application\'s theme has been changed to ' + object.title + "!")
        if not defaultTheme:
            object.is_default = True
        object.save()
admin.site.register(Theme, ThemeAdmin)


class UserThemeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'theme', 'pub_date']
    readonly_fields = ['user', 'theme']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(UserTheme, UserThemeAdmin)


class CookiePolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_date', 'modified_date', 'active']
admin.site.register(CookiePolicy, CookiePolicyAdmin)


class PlatformCommunityMemberAdmin(admin.ModelAdmin):
    """Manage the requests from authenticated users to join in platform community for support purposes"""

    list_display = ['user', 'fee', 'currency',
                    'is_professional', 'is_volunteer', 'skype', 'is_active']
    list_filter = ['is_professional',
                   'is_volunteer', 'is_active', 'joined_date', ]
    fields = ['user', ('fee', 'currency'), ('is_professional',
                                            'is_volunteer'), 'skype', 'is_active']
    readonly_fields = ['user', 'fee', 'currency',
                       'is_professional', 'is_volunteer', 'skype']
    ordering = ['user', ]

    def save_model(self, request, object, form, change):
        # Accept or reject the user request and inform him/her with email
        if object.is_active == True:
            content = _("Dear %s,\n\nI would like to inform you that your request has been accepted. From now, you are member of the our platform community that is aiming to provide support in other users.\n\nSincerely,\nThe administration team")\
                % (object.user.username)
            messages.add_message(request, messages.SUCCESS, 'The request of the ' +
                                 object.user.username + " has been accepted!")
        else:
            content = _("Dear %s,\n\nI would like to inform you that your request has been rejected. \n\nSincerely,\nThe administration team")\
                % (object.user.username)
            messages.add_message(request, messages.WARNING, 'The request of the ' +
                                 object.user.username + " has been rejected!")
        sendEmail([str(object.user.email)], _(
            "[P4ALL] Platform Community: request progress"), content, False)
        object.save()

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(PlatformCommunityMember, PlatformCommunityMemberAdmin)


class EvaluationMetricAdmin(admin.ModelAdmin):
    """Manage evaluation metrics of a service"""

    list_display = ['name', 'weight', 'min_score', 'max_score', 'is_active', ]
    list_filter = ['weight', 'min_score', 'max_score', 'is_active', ]
    fields = ['name', 'description',
              ('weight', 'min_score', 'max_score'), 'is_active', ]
    search_fields = ['name', ]
    ordering = ['weight', 'is_active', ]
    list_per_page = 10

admin.site.register(EvaluationMetric, EvaluationMetricAdmin)


class TermsUsageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_date', 'modified_date', 'active']

    def save_model(self, request, object, form, change):
        defaultTheme = TermsUsage.objects.filter(active=True).count()
        if object.active:
            TermsUsage.objects.filter(active=True).update(active=False)
            messages.add_message(request, messages.SUCCESS,
                                 'The terms of usage have been changed!')
        if not defaultTheme:
            object.active = True
        object.save()
admin.site.register(TermsUsage, TermsUsageAdmin)


##########################
##      TRANSLATION     ##
##########################
class TranslatedComponentsAdmin(ComponentsAdmin, TabbedTranslationAdmin):
    pass
admin.site.unregister(Components)
admin.site.register(Components, TranslatedComponentsAdmin)


class TranslatedCategoriesAdmin(CategoryAdmin, TabbedTranslationAdmin):
    pass
admin.site.unregister(Categories)
admin.site.register(Categories, TranslatedCategoriesAdmin)


class TranslatedTagsAdmin(TagAdmin, TabbedTranslationAdmin):
    pass
admin.site.unregister(Tags)
admin.site.register(Tags, TranslatedTagsAdmin)


class TranslatedItExperienceAdmin(ItExperienceAdmin, TranslationAdmin):
    pass
admin.site.unregister(ItExperience)
admin.site.register(ItExperience, TranslatedItExperienceAdmin)


class TranslatedChargingPoliciesAdmin(ChargingPoliciesAdmin, TranslationAdmin):
    pass
admin.site.unregister(ChargingPolicies)
admin.site.register(ChargingPolicies, TranslatedChargingPoliciesAdmin)


class TranslatedServicesAdmin(ServiceAdmin, TranslationAdmin):
    pass
admin.site.unregister(Services)
admin.site.register(Services, TranslatedServicesAdmin)


class TranslatedServiceKeywordsAdmin(ServiceKeywordAdmin, TranslationAdmin):
    pass
admin.site.unregister(ServiceKeywords)
admin.site.register(ServiceKeywords, TranslatedServiceKeywordsAdmin)


class TranslatedServiceConfigurationAdmin(ServiceConfigurationAdmin, TranslationAdmin):
    pass
admin.site.unregister(ServiceConfiguration)
admin.site.register(ServiceConfiguration, TranslatedServiceConfigurationAdmin)


class TranslatedTechnicalSupportAdmin(TechnicalSupportAdmin, TranslationAdmin):
    pass
admin.site.unregister(TechnicalSupport)
admin.site.register(TechnicalSupport, TranslatedTechnicalSupportAdmin)


class TranslatedServicesToTechnicalSupportAdmin(ServicesToTechnicalSupportAdmin, TranslationAdmin):
    pass
admin.site.unregister(ServicesToTechnicalSupport)
admin.site.register(ServicesToTechnicalSupport,
                    TranslatedServicesToTechnicalSupportAdmin)


class TranslatedNasConfigurationAdmin(NasConfigurationAdmin, TranslationAdmin):
    pass
admin.site.unregister(NasConfiguration)
admin.site.register(NasConfiguration, TranslatedNasConfigurationAdmin)


class TranslatedTopicAdmin(TopicAdmin, TranslationAdmin):
    pass
admin.site.unregister(Topic)
admin.site.register(Topic, TranslatedTopicAdmin)


class TranslatedArticleAdmin(ArticleAdmin, TranslationAdmin):
    pass
admin.site.unregister(Article)
admin.site.register(Article, TranslatedArticleAdmin)


class TranslatedArticleDocumentAdmin(ArticleDocumentAdmin, TranslationAdmin):
    pass
admin.site.unregister(ArticleDocument)
admin.site.register(ArticleDocument, TranslatedArticleDocumentAdmin)


class TranslatedArticleVideoAdmin(ArticleVideoAdmin, TranslationAdmin):
    pass
admin.site.unregister(ArticleVideo)
admin.site.register(ArticleVideo, TranslatedArticleVideoAdmin)


class TranslatedCookiePolicyAdmin(CookiePolicyAdmin, TranslationAdmin):
    pass
admin.site.unregister(CookiePolicy)
admin.site.register(CookiePolicy, TranslatedCookiePolicyAdmin)


class TranslatedEvaluationMetricAdmin(EvaluationMetricAdmin, TranslationAdmin):
    pass
admin.site.unregister(EvaluationMetric)
admin.site.register(EvaluationMetric, TranslatedEvaluationMetricAdmin)


class TranslatedTermsUsagedmin(TermsUsageAdmin, TranslationAdmin):
    pass
admin.site.unregister(TermsUsage)
admin.site.register(TermsUsage, TranslatedTermsUsagedmin)
