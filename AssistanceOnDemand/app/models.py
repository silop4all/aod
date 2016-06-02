"""
Definition of models.
"""

from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.

class Components(models.Model):
    """
    Depict the AoD components 
    """
    name = models.CharField(max_length=127, blank=False, null=False, unique=True)
    description = models.TextField(null=False, blank=False)
    is_enabled  = models.BooleanField(default=False, blank=False, null=False)

    def __unicode__(self):
        return self.name


class ItExperience(models.Model):
    """
    Store the levels of users' familiarity with IT services 
    """

    level = models.CharField(max_length=63, blank=False)
    description = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ["level"]
        db_table = "app_it_experience"


class Tags(models.Model):
    """
    Store a set of tags/keywords that describe the Categories' instances
        - Relationship: One tag is associated with M categories
    """

    title = models.CharField(max_length=128, null=False, blank=False, unique=True)

    def __unicode__(self):
        """ Get the tag's title """
        return self.title


class Categories(models.Model):
    """
    Store a list of categories that characterize the services
        - Relationship: One category contains N tags
        - Tree-view of categories
    """
    
    title       = models.CharField(max_length=128, null=False, blank=False, unique=False)
    description = models.CharField(max_length=300, null=False, blank=False)
    category    = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')
    question    = models.CharField(max_length=255, null=False, blank=False, unique=False)
    # derive an intermediate table due to the many-to-many relationship
    tags        = models.ManyToManyField(Tags)

    def __unicode__(self):
        """ Get the category's title """
        return self.title


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
    country = models.CharField(max_length=128, blank=False, default="Greek")
    city = models.CharField(max_length=128, blank=False, null=True)
    address = models.CharField(max_length=255, blank=False, null=True)
    postal_code = models.CharField(max_length=16, blank=False, null=True)
    logo = models.ImageField(upload_to='app/users/logos', blank=True, null=False) 
    cover = models.ImageField(upload_to='app/users/covers', blank=True, null=False) 
    experience = models.ForeignKey(ItExperience)
    categories = models.ManyToManyField(Categories)
    #registration = models.DateTimeField('registration date', blank=False, null=False, default=timezone.now())
    registration = models.DateTimeField('registration date', null=False, default=timezone.now)
    last_login = models.DateTimeField('last login', default=timezone.now)
    is_active = models.BooleanField(default=False, blank=False, null=False)

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
        """ Get the user ID """
        return self.id


class Providers(UserRole):
    """
    Store the list of users that provide services in the AoD platform
    """
    company = models.CharField(max_length=128, null=True, blank=False)
    pass


class Consumers(UserRole):
    """
    Store a list of users that consume services from the AoD platform
    """
    pass


class Carers(models.Model):
    """
    Store a list of registered users as carers that assist at least a consumer
    """
    
    user = models.ForeignKey(Users)
    is_active = models.BooleanField(default=False, blank=False, null=False)

    def __unicode__(self):
        """ Get the user ID """
        return self.id


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
        db_table = "app_carers_assist_consumers"


class ChargingPolicies(models.Model):
    """
    Store the supported charging policies by Assistance On Demand platform
    """
    
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)

    class Meta:
        db_table = "app_charging_policies"

    def __unicode__(self):
        return self.name
    
       
class Services(models.Model):
    """
    Store a list of offered services
    """
    
    MY_CHOICES = (('H', 'Human Based'),("M", "Machine Based"))

    title = models.CharField(max_length=128, null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='app/services/images', blank=True, null=False)  
    version = models.CharField(max_length=10, blank=False, null=True)
    license = models.CharField(max_length=30, blank=False, null=True)
    cover = models.CharField(max_length=128, blank=True, null=False)   
    type = models.CharField(max_length=1, choices = MY_CHOICES)
    categories = models.ManyToManyField(Categories)
    charging_policy = models.ForeignKey(ChargingPolicies)
    owner = models.ForeignKey(Providers)
    price = models.FloatField(blank=False, null=True)   # null cost means FREE??
    unit = models.TextField(max_length=10, null=False, blank=False)
    requirements = models.TextField(max_length=500, null=False, blank=False)        
    installation_guide = models.TextField(null=True, blank=False)
    software = models.FileField(upload_to='app/services/packages', blank=True, null=False)
    link = models.CharField(max_length=100, blank=False, null=True)
    usage_guidelines = models.TextField(blank=False, null=True)
    availability = models.BooleanField(max_length=1, default=True, blank=False, null=False) # True->global
    # target group of users or none
    constraints = models.TextField(null=True, blank=False)
    location_constraint = models.BooleanField(default=True, blank=False, null=False)
    latitude = models.FloatField(blank=False, null=False, default=0.0)
    longitude = models.FloatField(blank=False, null=False, default=0.0)
    coverage = models.FloatField(null=False, default=0.0)
    skype = models.CharField(max_length=63, null=True, default='')
    language_constraint = models.BooleanField(default=True, blank=False, null=False)
    is_available = models.BooleanField(max_length=1, default=True, blank=False, null=False)
    #created_date = models.DateTimeField(blank=False, null=False, default=datetime.now())
    #modified_date = models.DateTimeField(blank=False, null=False, default=datetime.now()) 
    created_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    modified_date = models.DateTimeField(blank=False, null=False, default=timezone.now) 

        


    def __unicode__(self):
        return "%s  (%s %s)" % (self.title, self.price, self.unit)


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
        db_table = "app_services_keywords"
        ordering = ["service_id"]

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
        db_table = "app_services_languages"
        ordering = ["service_id"]

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
        db_table = "app_services_configuration"
        ordering = ["service_id"]


class TechnicalSupport(models.Model):
    """
    Store a list of technical support types such as documents, video etc
    """

    type        = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(null=True, blank=False)

    class Meta:
        db_table = "app_technical_support_types"
        ordering = ["type"]

    def __unicode__(self):
        return self.type    


class ServicesToTechnicalSupport(models.Model):
    """
    Associate every service with the multiple types of technical support
    """

    service             = models.ForeignKey(Services, related_name="technical_support")
    technical_support   = models.ForeignKey(TechnicalSupport)
    title               = models.CharField(max_length=255, null=False) 
    format              = models.CharField(max_length=15)
    path                = models.CharField(max_length=255, null=False, blank=False, unique=False)
    software_dependencies = models.TextField(null=True, blank=False)

    class Meta:
        db_table = "app_services_technical_support"
        ordering = ["service", "technical_support"]

    def __unicode__(self):
        return self.id    


class ConsumersToServices(models.Model):
    """
    Associate the services which every consumer uses.
    """

    consumer = models.ForeignKey(Consumers)
    service = models.ForeignKey(Services)
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



