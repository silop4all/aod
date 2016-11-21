# -*- coding: utf-8 -*-

"""
Django deployment settings for AssistanceOnDemand project.

VARIABLES TO BE DEFINED:
    PRODUCTION
    SECRET_KEY
    EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD
    GOOGLE_ANALYTICS_PROPERTY_ID
    ANALYTICAL_INTERNAL_IPS
    GOOGLE_MAPS_KEY
    OPENAM_INTEGRATION
        CLIENT_ID* (if OPENAM_INTEGRATION = True)
        CLIENT_SECRET* (if OPENAM_INTEGRATION = True)
        OAUTH_SERVER* (if OPENAM_INTEGRATION = True)
    SOCIAL_NETWORK_URL
    SOCIAL_NETWORK_WEB_SERVICES
    SOCIAL_NETWORK_WEB_SERVICES_AUTH
    CROWD_FUNDING
"""

from os import path
from django.utils.translation import ugettext_lazy as _

#==================================
#   PROJECT ROOT 
#==================================
PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

#==================================
#   EXECUTION MODE     
#==================================
PRODUCTION = False
if PRODUCTION:
    try:
        from production_settings import *
    except ImportError:
        raise ImportError('The production_settings.py file does not exist')
else:
    try:
        from development_settings import *
    except ImportError:
        raise ImportError('The development_settings.py file does not exist')


#==================================
#   TEMPLATES CONFIGURATION 
#==================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.core.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'app.context_processors.app_processor',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                #
                "django.core.context_processors.request",
                "django.core.context_processors.media",
                #"admin_tools.template_loaders.TemplateLoader" # or commented
            ]  ,
            "debug": DEBUG,
        },
    },
]
"""
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "admin_tools.template_loaders.TemplateLoader"
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
 List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)
"""

#==================================
#   MIDDLEWARES MANAGEMENT      
#==================================
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',    
    'app.middleware.multilingual.SyncLanguageCookie'
)

#==================================
#   BASIC SETTINGS
#==================================
LOGIN_URL = '/login'
SITE_ID = 1
ROOT_URLCONF = 'AssistanceOnDemand.urls'
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'AssistanceOnDemand.wsgi.application'
# Make this unique, and don't share it with anybody.
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Generate it http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = {SECRET_KEY}

#=================================
#   TIMEZONE SETTINGS           
#=================================
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Athens'
# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#=================================
#   MULTILINGUAL SETTINGS       
#=================================
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGES = (
    ('el', _('Greek')),
    ('en', _('English')),
    ('it', _('Italian')),
    ('es', _('Spanish')),
    ('fr', _('French')),
    ('de', _('German')),
)
# Default language
LANGUAGE_CODE = 'en'
# Cookie settings for language
LANGUAGE_COOKIE_NAME = "aod_language"
LANGUAGE_COOKIE_AGE = 365*24*60*60      # 1 year
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

#=================================
#   LOCALE FILES SETTINGS      
#=================================
LOCALE_PATHS = ( 
    path.join(PROJECT_ROOT, 'locale'), 
)

#=================================
#   MEDIA FILES SETTINGS      
#=================================
MEDIA_ROOT = path.join(PROJECT_ROOT, 'media').replace('\\', '/')
MEDIA_URL = AOD_HOST['PATH'] + '/media/'

#=================================
#   STATIC FILES SETTINGS     
#=================================
STATIC_ROOT = path.join(PROJECT_ROOT, 'static').replace('\\', '/')
STATIC_URL = AOD_HOST['PATH'] + '/static/'
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # mine
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # 'compressor.finders.CompressorFinder',
)

#==================================
#   LOGGING MANAGEMENT      
#==================================
# Send email on admin in case of non handled exceptions
# See http://docs.djangoproject.com/en/dev/topics/logging 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(PROJECT_ROOT) + '/debug.log',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(PROJECT_ROOT) + '/error.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#==================================
#   TEST RUNNER CONFIGURATION  
#==================================
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

#=================================
#   AOD EMAIL ACCOUNT           
#=================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = {EMAIL_HOST_USER}
EMAIL_HOST_PASSWORD = {EMAIL_HOST_PASSWORD}
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#==================================
#   UPLOADED SERVICES SETTINGS
#==================================
SERVICES_IMAGE_PATH = "app/services/images/"
SERVICES_TECHNICAL_SUPPORT = "app/services/technical-support/"

#==================================
#   PRESENTATION THEME COOKIE
#==================================
THEME_COOKIE_NAME = "aod_theme"

#==================================
#   GRAPPELLI THEME SETTINGS   
#==================================
GRAPPELLI_ADMIN_TITLE = _("AoD administration panel")
#GRAPPELLI_CLEAN_INPUT_TYPES = False

#==================================
#   DRF CONFIGURATION          
#==================================
# Support JSON/XML/YAML parsers
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework_xml.parsers.XMLParser',
        'rest_framework_yaml.parsers.YAMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework_yaml.renderers.YAMLRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}

#==================================
#   SWAGGER CONFIGURATION
#==================================
SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '1.0',
    'api_path': '/',
    'base_path': str(AOD_HOST['IP']) + ":" + str(AOD_HOST['PORT']) + str(AOD_HOST['PATH']) + "/" + str(LANGUAGE_CODE) + '/docs',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete',
        'options'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    #'permission_denied_handler': None,
    #'resource_access_handler': None,
    'info': {
        'contact': DEVELOPER_EMAIL,
        'description': _('Find below the documentation of REST web services that AoD provides.'),
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'title': _('Documentation of AoD web services'),
    },
    'doc_expansion': 'none',
}

#==================================
#   GRAPH MODELS SETTINGS      
#==================================
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

#==================================
#   ROSETTA SETTINGS      
#==================================
ROSETTA_MESSAGES_PER_PAGE = 10
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
#ROSETTA_ENABLE_REFLANG = True

#==================================
#   GOOGLE ANALYTICS SETTINGS      
#==================================
GOOGLE_ANALYTICS_PROPERTY_ID = {GOOGLE_ANALYTICS_PROPERTY_ID}
ANALYTICAL_INTERNAL_IPS = [AOD_HOST['IP']]
ANALYTICAL_AUTO_IDENTIFY = False
GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = True

#==================================
#   GOOGLE MAPS KEY  
#==================================
GOOGLE_MAPS_KEY = {GOOGLE_MAPS_KEY}

#==================================
#   CORS ORIGIN SETTINGS      
#==================================
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

#==================================
#   ADMIN IMPORT/EXPORT SETTINGS
#==================================
IMPORT_EXPORT_USE_TRANSACTIONS = True

#==================================
#   MODEL-TRANSLATION SETTINGS
#==================================
MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE
MODELTRANSLATION_AUTO_POPULATE = True
MODELTRANSLATION_DEBUG = False
MODELTRANSLATION_ENABLE_FALLBACKS = True
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': tuple([v[0] for i,v in enumerate(LANGUAGES)])
}

#==================================
#   CKEDITOR SETTINGS
#==================================
CKEDITOR_UPLOAD_PATH = "admin/ckeditor/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_UPLOAD_SLUGIFY_FILENAME= True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Advanced',
        'width': 'auto',
        "removePlugins": "stylesheetparser",
        'tabSpaces': 4,
        #'uiColor': '#9AB8F3',
        'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'toolbarCanCollapse': True,
        'extraPlugins': ','.join(['autolink','embedsemantic','embedbase','xml', 'preview','sharedspace'])
    }
}

#==================================
#   FILEBROWSER SETTINGS
#==================================
FILEBROWSER_DIRECTORY = 'admin/filebrowser/'
FILEBROWSER_EXTENSIONS = {
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Document': ['.pdf','.doc','.docx','.txt','.xls','.xlsx', '.ppt', '.pptx','.csv'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.mp4'],
    'Audio': ['.mp3','.mp4','.wav','.m4p'],
}
FILEBROWSER_SELECT_FORMATS  = {
    'file': ['Image','Document','Video','Audio'],
    'image': ['Image'],
    'document': ['Document'],
    'media': ['Video','Audio'],
}
FILEBROWSER_VERSIONS_BASEDIR = 'admin/_versions'
FILEBROWSER_VERSIONS = {
    'admin_thumbnail': {'verbose_name': _('Admin Thumbnail'), 'width': 60, 'height': 60, 'opts': 'crop'},
    'thumbnail': {'verbose_name': _('Thumbnail (1 col)'), 'width': 60, 'height': 60, 'opts': 'crop'},
    'small': {'verbose_name': _('Small (2 col)'), 'width': 140, 'height': '', 'opts': ''},
    'medium': {'verbose_name': _('Medium (4col )'), 'width': 300, 'height': '', 'opts': ''},
    'big': {'verbose_name': _('Big (6 col)'), 'width': 460, 'height': '', 'opts': ''},
    'large': {'verbose_name': _('Large (8 col)'), 'width': 680, 'height': '', 'opts': ''},
}
FILEBROWSER_ADMIN_VERSIONS = ['thumbnail', 'small', 'medium', 'big', 'large']
FILEBROWSER_VERSION_PROCESSORS = [
    'filebrowser.utils.scale_and_crop',
]
FILEBROWSER_PLACEHOLDER = _("upload a file")
FILEBROWSER_IMAGE_MAXBLOCK = 1024*1024
FILEBROWSER_MAX_UPLOAD_SIZE = 5242880       # 5 MB
FILEBROWSER_LIST_PER_PAGE = 10
FILEBROWSER_CONVERT_FILENAME = True
FILEBROWSER_FOLDER_REGEX = r'^[\w._\ /-]+$'
FILEBROWSER_DEFAULT_PERMISSIONS = 0o755
FILEBROWSER_VERSION_NAMER = 'filebrowser.namers.VersionNamer'
FILEBROWSER_SHOW_PLACEHOLDER = True
FILEBROWSER_OVERWRITE_EXISTING = False

#==================================
#   DEBUG TOOLBAR SETTINGS      
#==================================
#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.version.VersionDebugPanel',
#    'debug_toolbar.panels.timer.TimerDebugPanel',
#    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#    'debug_toolbar.panels.headers.HeaderDebugPanel',
#    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#    'debug_toolbar.panels.template.TemplateDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#    'debug_toolbar.panels.signals.SignalDebugPanel',
#    'debug_toolbar.panels.logger.LoggingPanel',
#)

#==================================
#   CACHE SETTINGS      
#==================================
# pip install pylibmc
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}
#def get_cache():
#  import os
#  try:
#    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
#    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
#    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
#    return {
#      'default': {
#        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#        'TIMEOUT': 500,
#        'BINARY': True,
#        'OPTIONS': { 'tcp_nodelay': True }
#      }
#    }
#  except:
#    return {
#      'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
#      }
#    }
#CACHES = get_cache()

#==================================
#   CONSTANCE SETTINGS      
#==================================
#CONSTANCE_CONFIG = {
#    'THE_ANSWER': (42, 'Answer to the Ultimate Question of Life, '
#                       'The Universe, and Everything'),
#}
#CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True



#=================================
#   INTEGRATION with IAM      
#=================================
OPENAM_INTEGRATION = False
CLIENT_ID = {CLIENT_ID_In_OPENAM}
CLIENT_SECRET = {CLIENT_SECRET_IN_OPENAM}
OAUTH_SERVER = {IP:PORT}
CALLBACK_URL = '/callback/openam'
REDIRECT_URL = AOD_HOST['PROTOCOL'] + "://" + AOD_HOST['IP'] + ':' + str(AOD_HOST['PORT']) + AOD_HOST['PATH'] + CALLBACK_URL

#==================================
#   INTEGRATION WITH SOCIAL NETWORK
#==================================
# enable/disable it via administration panel (app components)
SOCIAL_NETWORK_URL = "http://localhost:40000/aodsocial/app/#/home"
SOCIAL_NETWORK_WEB_SERVICES = {
    "url": "localhost:8080",
    "base": "http://localhost:8080",
    "services": {
        "insert": "/api/jsonws/aodsocial-portlet.aodsocial/on-register-aod-service/service-id/",
        "delete": "/api/jsonws/aodsocial-portlet.aodsocial/on-delete-aod-service/service-id/"
    },
    "users": {
        "insert": "/api/jsonws/aodsocial-portlet.aodsocial/login-with-register"
    },
    "sessions":{
        "logout": "/api/jsonws/aodsocial-portlet.aodsocial/propagate-logout/aod-user-id/"
    }
}
SOCIAL_NETWORK_WEB_SERVICES_AUTH = {SOCIAL_NETWORK_WEB_SERVICES_AUTH}

#==================================
#   INTEGRATION WITH CROWD FUNDING
#==================================
# enable/disable it via administration panel (app components)
CROWD_FUNDING = {
    "base": "http://localhost",
    "projects": {
        "insert": "/proposal/new"
    }
}

#==================================
#   CUSTOMIZATION STATE
#==================================
CUSTOMIZATION_PROCESS = True