# -*- coding: utf-8 -*-

"""
Definition of models.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext as _
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import (
    RichTextUploadingField, 
    RichTextUploadingFormField
)
from filebrowser.fields import FileBrowseField
from colorful.fields import RGBColorField


TYPE_CHOICES = (
    ('H', _('Human Based')),
    ("M", _("Machine Based"))
)

class Logo(models.Model):
    """
    Keep the application logo
    """
    title       = models.CharField(max_length=32, blank=False, null=False)
    placeholder = models.CharField(max_length=96, blank=False, null=False, default="Welcome in platform")
    logo        = FileBrowseField(_("logo"), max_length=500, directory="logos", extensions=settings.FILEBROWSER_EXTENSIONS['Image'], blank=False, null=False)
    selected    = models.BooleanField(default=False, blank=False, null=False)

    class Meta :
        verbose_name = _("App Logo")
        verbose_name_plural = _("App Logos")

    def __unicode__(self):
        """ Get the title """
        return self.title


class Favicon(models.Model):
    """
    Keep the application favicon
    """
    title = models.CharField(max_length=32, blank=False, null=False)
    favicon = FileBrowseField(_("favicon"), max_length=500, directory="favicons", extensions=settings.FILEBROWSER_EXTENSIONS['Image'], blank=False, null=False)
    selected = models.BooleanField(default=False, blank=False, null=False)

    class Meta :
        verbose_name = _("App Favicon")
        verbose_name_plural = _("App Favicons")

    def __unicode__(self):
        """ Get the title """
        return self.title


class Metadata(models.Model):
    """
    Keep the content of HTML meta elements
    """
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(blank=False, null=False, help_text="Enter the application's description that is included in HTML meta element with `name` -> `description`")
    keywords = models.CharField(max_length=128, blank=False, null=False, help_text="Enter the application's keywords that are included in the HTML meta element with `name` -> `keywords`")
    author = models.CharField(max_length=32, blank=False, null=False, help_text="Enter the application's author that is included in the HTML meta element with `name` -> `author`")
    active = models.BooleanField(default=True, null=False, blank=False)

    class Meta :
        verbose_name = _("App Metadata")
        verbose_name_plural = _("App Metadata")

    def __unicode__(self):
        """ Get the title """
        return self.title


class SocialNetwork(models.Model):
    """
    Keep the links of social networks related to the app
    """
    title   = models.CharField(max_length=32, blank=False, null=False)
    url     = models.URLField(blank=True, null=True)
    visible = models.BooleanField(default=True, blank=False, null=False)
    
    class Meta :
        verbose_name = _("Social Network")
        verbose_name_plural = _("Social Networks")

    def __unicode__(self):
        """ Get the title """
        return self.title


class Components(models.Model):
    """
    Depict the AoD components 
    """
    name = models.CharField(max_length=127, blank=False, null=False, unique=True)
    description = models.TextField(null=False, blank=False)
    is_enabled  = models.BooleanField(default=False, blank=False, null=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("App Component")
        verbose_name_plural = _("App Components")


class LanguageFlag(models.Model):
    alias   = models.CharField(max_length=4, blank=False, null=False, unique=True)
    flag    = FileBrowseField(_("flag"), max_length=500, directory="languages", extensions=settings.FILEBROWSER_EXTENSIONS['Image'], blank=False, null=False)

    class Meta :
        verbose_name = _("App Language Flag")
        verbose_name_plural = _("App Language Flags")

    def __unicode__(self):
        """ Get the title """
        return self.alias


class ContactUs(models.Model):
    """
    Store the contact details of the application
    """
    skype_id = models.CharField(max_length=64, null=False, blank=False, unique=True, help_text="Hint: Entert the Skype id that characterizes the application")
    skype_button_id = models.CharField(max_length=255, null=False, blank=False, unique=True, help_text="Hint: Enter the string that is generated from skype online service. It is included to JS file to be displayed the skype button")
    phone = models.CharField(max_length=15, null=False, blank=False, help_text="Hint: Enter the phone number for contact purposes")
    email = models.EmailField(max_length=100, null=False, blank=False, help_text="Hint: Enter the email account that users can access")
    address = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        db_table            = "app_contact_us"
        verbose_name        = _("App contact details")
        verbose_name_plural = _("App contact details")


class IncomingQuestions(models.Model):
    """
    Store the questions of registered or anonymous users
    """
    user = models.CharField(max_length=128, null=False, blank=False, help_text="Name and lastname of user/visitor")
    email = models.EmailField(max_length=128, null=False, blank=False, help_text="Email info of user")
    topic = models.CharField(max_length=64, null=False, blank=False, help_text="The thematic area of question")
    message = models.TextField(max_length=500, null=False, blank=False, help_text="The question of the user")
    pub_date = models.DateTimeField(blank=False, null=False, auto_now=True)

    class Meta:
        db_table            = "app_questions"
        verbose_name        = _("App incoming question")
        verbose_name_plural = _("App incoming questions")


class ItExperience(models.Model):
    """
    Store the levels of users' familiarity with IT services 
    """

    level = models.CharField(max_length=63, blank=False)
    description = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering            = ["level"]
        db_table            = "app_it_experience"
        verbose_name        = _("IT skill level")
        verbose_name_plural = _("IT skill levels")


class Tags(models.Model):
    """
    Store a set of tags/keywords that describe the Categories' instances
        - Relationship: One tag is associated with M categories
    """

    title = models.CharField(max_length=128, null=False, blank=False, unique=True)

    def __unicode__(self):
        """ Get the tag's title """
        return self.title

    class Meta:
        verbose_name        = _("Tag")
        verbose_name_plural = _("Tags")


class Categories(models.Model):
    """
    Store a list of categories that characterize the services
        - Relationship: One category contains N tags
        - Tree-view of categories
    """
    
    title       = models.CharField(max_length=128, null=False, blank=False, unique=False)
    description = models.CharField(max_length=300, null=False, blank=False)
    category    = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank = True, related_name='children')
    question    = models.CharField(max_length=255, null=False, blank=False, unique=False)
    # derive an intermediate table due to the many-to-many relationship
    tags        = models.ManyToManyField(Tags)

    def __unicode__(self):
        """ Get the category's title """
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Users(models.Model):
    """
    Store a collection of AoD users which have any role to it.
    """
    
    GENDER_CHOICES = (('M', 'Mr'),("W", "Miss"))

    name = models.CharField(max_length=63, blank=False, null=False)
    lastname = models.CharField(max_length=63, blank=False, null=False)
    gender = models.CharField(max_length=1, choices = GENDER_CHOICES)
    username = models.CharField(max_length=127, blank=False, unique=True, null=False)
    pwd = models.CharField(max_length=128, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    mobile = models.CharField(max_length=15, blank=False, default="000000000000000")
    country = models.CharField(max_length=128, blank=False, default="Greece")
    city = models.CharField(max_length=128, blank=False, null=True)
    address = models.CharField(max_length=255, blank=False, null=True)
    postal_code = models.CharField(max_length=16, blank=False, null=True)
    logo = models.ImageField(upload_to='app/users/logos', blank=True, null=False) 
    cover = models.ImageField(upload_to='app/users/covers', blank=True, null=False) 
    experience = models.ForeignKey(ItExperience)
    categories = models.ManyToManyField(Categories)
    registration = models.DateTimeField('registration date', null=False, default=timezone.now)
    last_login = models.DateTimeField('last login', default=timezone.now)
    is_active = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __unicode__(self):
        """ Get the username of user """
        return "%s %s (%s)" % (self.name, self.lastname, self.username)


class UserRole(models.Model):
    """ 
    Define class as abstract. That means:
        - None MySQL table is created
        - Can not be instantiated or saved directly
        - It's used only for inheritance issues
    """

    user = models.ForeignKey(Users)
    crowd_fund_participation = models.BooleanField(default=True, blank=False, null=False)
    crowd_fund_notification = models.BooleanField(default=True, blank=False, null=False)
    is_active = models.BooleanField(default=False, blank=False, null=False)
    
    
    class Meta:
        abstract=True
        ordering = ["id"]

    def __unicode__(self):
        """ Get the user """
        return self.user.username


class Providers(UserRole):
    """
    Store the list of users that provide services in the AoD platform
    """
    company = models.CharField(max_length=128, null=True, blank=False)
    
    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")


class Consumers(UserRole):
    """
    Store a list of users that consume services from the AoD platform
    """
    class Meta:
        verbose_name = _("Consumer")
        verbose_name_plural = _("Consumers")


class Carers(models.Model):
    """
    Store a list of registered users as carers that assist at least a consumer
    """
    
    user = models.ForeignKey(Users)
    is_active = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = _("Carer")
        verbose_name_plural = _("Carers")

    def __unicode__(self):
        """ Get the user """
        return self.user.name


class CarersAssistConsumers(models.Model):
    """
    Associate each carer with the consumers for which is responsible to setup a network of assistance services
    """
    
    carer       = models.ForeignKey(Carers)
    consumer    = models.ForeignKey(Consumers)
    # consumer response event (1->true)
    response    = models.BooleanField(default=False, blank=False, null=False)
    # consumer response (1->grant privileges)
    state       = models.BooleanField(default=False, blank=False, null=False)
    #created_at  = models.DateTimeField(auto_now_add=True)
    created_at  = models.DateTimeField(blank=False, null=False, default="1970-01-01 00:00:00")
    updated_at  = models.DateTimeField(blank=False, null=False, default="1970-01-01 00:00:00", auto_now_add=False) 

    class Meta:
        db_table            = "app_carers_assist_consumers"
        verbose_name        = _("Carer Assist Consumer")
        verbose_name_plural = _("Carers Assist Consumers")


class ChargingPolicies(models.Model):
    """
    Store the supported charging policies by Assistance On Demand platform
    """
    
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)

    class Meta:
        db_table            = "app_charging_policies"
        verbose_name        = _("Charging Policy")
        verbose_name_plural = _("Charging Policies")

    def __unicode__(self):
        return self.name


class Services(models.Model):
    """
    Store a list of offered services
    """

    title = models.CharField(max_length=128, null=False, blank=False, unique=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to=settings.SERVICES_IMAGE_PATH, blank=True, null=False)  
    version = models.CharField(max_length=10, blank=True, null=True, help_text=_("Define the version of the service if it is machine-based one"))
    license = models.CharField(max_length=30, blank=True, null=True, help_text=_("Define the licenses of the service if it is machine-based one"))
    type = models.CharField(max_length=1, choices = TYPE_CHOICES)
    categories = models.ManyToManyField(Categories)
    charging_policy = models.ForeignKey(ChargingPolicies)
    owner = models.ForeignKey(Providers)
    price = models.FloatField(blank=False, null=True, default="0.0", help_text=_("Define the price of the service"))
    unit = models.TextField(max_length=10, null=False, blank=False)
    requirements = models.TextField(max_length=500, null=True, blank=True)
    installation_guide = models.TextField(null=True, blank=True)
    usage_guidelines = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(max_length=1, default=True, blank=False, null=False, help_text=_("Define the scope of the service; use True for public access on it or False to limit the users that can access it "))
    language_constraint = models.BooleanField(default=True, blank=False, null=False)
    location_constraint = models.BooleanField(default=True, blank=False, null=False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    coverage = models.FloatField(null=True, blank=True, help_text=_("The radius in km where the provider can offer this service"))
    constraints = models.TextField(null=True, blank=True, help_text=_("Free text to enter other constraints"))
    skype = models.CharField(max_length=63, null=True, blank=True)
    is_visible = models.BooleanField(max_length=1, default=True, blank=False, null=False, help_text=_('Click the checkbox if the provider wants to publish it in the platform'))
    created_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    modified_date = models.DateTimeField(blank=False, null=False, default=timezone.now) 

    # availability -> is_public
    # is_available -> is_visible
    #rm cover = models.CharField(max_length=128, blank=True, null=False)   
    #rm software = models.FileField(upload_to='app/services/packages', blank=True, null=False)
    #rm link = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name        = _("Service")
        verbose_name_plural = _("Services")

    def __unicode__(self):
        return self.title


class NasTemporarySetup(models.Model):
    """
    Store temporarily the current services that a carer selects on behalf of consumer and its timestamp. It works like a queue.
    """

    service     = models.ForeignKey(Services)
    carer       = models.ForeignKey(Carers)
    consumer    = models.ForeignKey(Consumers)
    created_at  = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    class Meta:
        db_table = "app_nas_temp_setup"
        ordering = ["created_at"]


class ServiceKeywords(models.Model):
    """
    Keywords that characterized a service
    """

    service = models.ForeignKey(Services, related_name='keywords')
    title = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table            = "app_services_keywords"
        ordering            = ["service_id"]
        verbose_name        = _("Service Keyword")
        verbose_name_plural = _("Service Keywords")

    def __unicode__(self):
        service = Services.objects.get(pk=self.service_id)
        return "%s: %s " % (service.title, self.title)


class ServiceLanguages(models.Model):
    """
    Languages that a service supports
    """

    service = models.ForeignKey(Services, related_name='languages')
    alias = models.CharField(max_length=10, null=False, blank=False)

    class Meta:
        db_table            = "app_services_languages"
        ordering            = ["service_id"]
        verbose_name_plural = _("Service Languages")

    def __unicode__(self):
        service = Services.objects.get(pk=self.service_id)
        return "%s: %s " % (service.title, self.alias)


class ServiceConfiguration(models.Model):
    """
    The configuration of a service that the provider registers
    """
    service     = models.ForeignKey(Services, related_name='configuration')
    parameter   = models.CharField(max_length=512, null=False, blank=False)
    value       = models.CharField(max_length=255, null=False, blank=False)
    is_default  = models.BooleanField(default=True, blank=False, null=False)

    class Meta:
        db_table            = "app_services_configuration"
        ordering            = ["service_id"]
        verbose_name        = _("Service Configuration")
        verbose_name_plural = _("Service Configuration")


class TechnicalSupport(models.Model):
    """
    Store a list of technical support types such as documents, video etc
    """

    type        = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    alias = models.CharField(max_length=32, blank=False, null=True)

    class Meta:
        db_table            = "app_technical_support_types"
        ordering            = ["type"]
        verbose_name        = _("Technical Support")
        verbose_name_plural = _("Technical Support")

    def __unicode__(self):
        return self.type    


class ServicesToTechnicalSupport(models.Model):
    """
    Associate every service with the multiple types of technical support
    """

    service = models.ForeignKey(Services, related_name="technical_support")
    technical_support = models.ForeignKey(TechnicalSupport)
    title = models.CharField(max_length=255, null=False) 
    description = models.TextField(null=True, blank=False)
    software_dependencies = models.TextField(null=True, blank=False)
    link = models.CharField(max_length=300, default="")
    #path = models.FileField(upload_to=settings.SERVICES_TECHNICAL_SUPPORT, default=settings.SERVICES_TECHNICAL_SUPPORT + '/test.pdf')
    path = models.TextField(default=settings.MEDIA_URL + settings.SERVICES_TECHNICAL_SUPPORT + '/test.pdf')
    extension = models.CharField(max_length=15, default="unknown")
    created_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    modified_date = models.DateTimeField(blank=False, null=False, auto_now=True)
    visible = models.BooleanField(default=True, blank=False, null=False)

    class Meta:
        db_table            = "app_services_technical_support"
        ordering            = ["service", "technical_support"]
        verbose_name_plural = _("Service Technical Support")

    def __unicode__(self):
        return self.id 


class ConsumersToServices(models.Model):
    """
    Associate the services which every consumer uses.
    """

    consumer = models.ForeignKey(Consumers)
    service = models.ForeignKey(Services, related_name='service_consumers')
    cost = models.FloatField(blank=False, null=True)   # null cost means FREE
    purchased_date = models.DateTimeField()
    rating = models.FloatField(blank=False, null=True)
    rating_rationale = models.TextField(blank=False, null=True)
    is_completed = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        db_table = "app_consumers_services"
        ordering = ["consumer", "service"]


class NasConsumersToServices(models.Model):
    consumer        = models.ForeignKey(Consumers)
    service         = models.ForeignKey(Services)
    cost            = models.FloatField(blank=False, null=True)   # null cost means FREE
    purchased_date  = models.DateTimeField()
    rating          = models.FloatField(blank=False, null=True)
    rating_rationale= models.TextField(blank=False, null=True)
    is_completed    = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        db_table = "app_nas_consumers_services"
        ordering = ["consumer", "service"]


class NasConfiguration(models.Model):
    """
    The configuration of a service that the carer selects (carer can overwrite the provider default settings)
    """
    nas         = models.ForeignKey(NasConsumersToServices, related_name='configuration')
    parameter   = models.CharField(max_length=512, null=False, blank=False)
    value       = models.CharField(max_length=255, null=False, blank=False)
    is_default  = models.BooleanField(default=True, blank=False, null=False)
    updated     = models.DateTimeField(null=False, default=datetime.now()) 

    class Meta:
        db_table = "app_network_services_configuration"
        ordering = ["nas"]


class Tokens(models.Model):
    """
    The access tokens in case of IAM/OPENAM usage
    """

    user            = models.ForeignKey(Users)
    access_token    = models.CharField(max_length=512, null=False, blank=False)
    refresh_token   = models.CharField(max_length=512, null=False, blank=False)
    expires_in      = models.IntegerField(null=False, blank=False)
    scope           = models.CharField(max_length=64, null=False, blank=False)
    token_type      = models.CharField(max_length=16, null=False, blank=False)
    
    class Meta:
        db_table            = "app_oauth2_tokens"
        verbose_name        = _("Token")
        verbose_name_plural = _("Tokens")


class Topic(models.Model):
    """ Topics for frequently asked Questions """
    title           = models.CharField(max_length=128, null=False, blank=False, unique=True)
    description     = models.CharField(max_length=512, null=True, blank=False)
    created_date    = models.DateTimeField(blank=False, null=True, default=timezone.now)
    modified_date   = models.DateTimeField(blank=False, null=True, auto_now=True)
    visible         = models.BooleanField(default=True, blank=False, null=False)
    protected       = models.BooleanField(default=False, blank=False, null=False)
    
    def __unicode__(self):
        return self.title

    class Meta:
        db_table            = "app_faq_topics"
        verbose_name        = _("Topic")
        verbose_name_plural = _("Topics")


class Article(models.Model):
    """ Article per F.A.Q. topic """
    title           = models.CharField(max_length=128, null=False, blank=False, unique=True)
    topic           = models.ForeignKey(Topic, related_name='articles')
    service         = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, blank=True, related_name="service")
    content         = RichTextUploadingField('contents')
    published_date  = models.DateTimeField(blank=False, null=True, default=timezone.now)
    modified_date   = models.DateTimeField(blank=False, null=False, auto_now=True)
    visible         = models.BooleanField(default=True, blank=False, null=False)
    protected       = models.BooleanField(default=False, blank=False, null=False)
        

    def __unicode__(self):
        return self.title

    class Meta:
        db_table            = "app_faq_articles"
        verbose_name        = _("Article")
        verbose_name_plural = _("Articles")


class ArticleDocument(models.Model):
    """
    Upload documents for articles
    """
    article         = models.ForeignKey(Article, related_name='docs')
    title           = models.CharField(max_length=64, null=False, blank=False, unique=True)
    description     = models.CharField(max_length=255, null=True, blank=True, unique=True)
    published_date  = models.DateTimeField(blank=False, null=False, auto_now=True)
    element         = FileBrowseField(_("document"), max_length=500, directory="support/documents", extensions=settings.FILEBROWSER_EXTENSIONS['Document'], blank=True, null=True)
    visible         = models.BooleanField(default=True, blank=False, null=False)
    protected       = models.BooleanField(default=False, blank=False, null=False)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table            = "app_articles_documents"
        verbose_name        = _("Article Document")
        verbose_name_plural = _("Article Documents")


class ArticleVideo(models.Model):
    """
    Upload videos for articles
    """
    article         = models.ForeignKey(Article, related_name='videos')
    title           = models.CharField(max_length=64, null=False, blank=False, unique=True)
    description     = models.CharField(max_length=255, null=True, blank=True, unique=True)
    published_date  = models.DateTimeField(blank=False, null=False, auto_now=True)
    element         = FileBrowseField(_("video"), max_length=500, directory="support/videos", extensions=settings.FILEBROWSER_EXTENSIONS['Video'], blank=True, null=True)
    visible         = models.BooleanField(default=True, blank=False, null=False)
    protected       = models.BooleanField(default=False, blank=False, null=False)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table            = "app_articles_videos"
        verbose_name        = _("Article Video")
        verbose_name_plural = _("Article Videos")


class Theme(models.Model):
    """
    Store details about the themes that app administrator uploads in static files
    """

    hint = [str(i) + " pixels" for i in range(0,21)]
    RADIUS_CHOICES = zip( range(0,21), hint )

    title           = models.CharField(max_length=32, null=False, blank=False, unique=True)
    url             = models.CharField(max_length=254, null=False, blank=False, unique=True, help_text="Help: Upload this css file in app/static/app/content/ directory and run python manage.py collectstatic --noinput cmd")
    success_base    = RGBColorField()
    primary_base    = RGBColorField()
    info_base       = RGBColorField()
    warning_base    = RGBColorField()
    danger_base     = RGBColorField()
    radius          = models.IntegerField(choices=RADIUS_CHOICES, blank=False, null=False, default=0)
    is_visible      = models.BooleanField(default=False, blank=False, null=False)
    is_default      = models.BooleanField(default=False, blank=False, null=False)
    created_date    = models.DateTimeField(blank=False, null=False, auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table            = "app_themes"
        verbose_name        = _("App Theme")
        verbose_name_plural = _("App Themes")


class UserTheme(models.Model):
    
    user        = models.ForeignKey(Users)
    theme       = models.ForeignKey(Theme)
    pub_date    = models.DateTimeField(blank=False, null=False, auto_now=True)

    def __unicode__(self):
        return self.theme.title

    class Meta:
        db_table            = "app_user_themes"
        unique_together     = ('user', 'theme',)
        verbose_name        = _("User Preferred Theme")
        verbose_name_plural = _("User Preferred Themes")


class CookiePolicy(models.Model):
    """Cookie policy content"""
    title = models.CharField(max_length=32, null=False, blank=False)
    content = RichTextUploadingField('contents')
    published_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    modified_date = models.DateTimeField(blank=False, null=False, auto_now=True)
    active = models.BooleanField(default=True, blank=False, null=False)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table            = "app_cookie_policy"
        verbose_name        = _("Cookie Policy")
        verbose_name_plural = _("Cookie Policy")



#===============
# payment dev
#===============
class PaypalCredentials(models.Model):
    """Keep the app credentials in paypal per provider
    """
    provider = models.ForeignKey(Providers)
    username = models.CharField(max_length=512, null=False, blank=False)
    password = models.CharField(max_length=512, null=False, blank=False)
    token = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.provider


class ServicePayment(models.Model):
    """Keep payment metadata per service (no recurring payments)"""
    service = models.ForeignKey(Services)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    handling_fee = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_discount = models.DecimalField(max_digits=10, decimal_places=2)
    insurance = models.DecimalField(max_digits=10, decimal_places=2)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.service.title

    class Meta:
        db_table            = "app_service_payment_details"
        verbose_name        = _("Service payment details")
        verbose_name_plural = verbose_name        