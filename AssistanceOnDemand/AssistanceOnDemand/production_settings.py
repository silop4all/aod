# -*- coding: utf-8 -*-

"""
Settings for production purposes

TO BE DEFINED:
    DEVELOPER_EMAIL
    EVALUATOR_EMAIL
    AOD_HOST
    DATABASES
"""

#=================================
#   DEBUG SETTINGS     
#=================================
# TEMPLATE_DEBUG @deprecated in django > 1.8
DEBUG = False

#=================================
#   EVALUATION CONTACT     
#=================================
EVALUATION_PROCESS  = False
DEVELOPER_EMAIL = {DEVELOPER_EMAIL}
EVALUATOR_EMAIL = {EVALUATOR_EMAIL}
RECEIVER_EMAIL = [EVALUATOR_EMAIL] if EVALUATION_PROCESS == True else [DEVELOPER_EMAIL]

#=================================
#   AOD HOST INFO           
#=================================
# Allowed path can be an empty string '' or string that starts
# with / char and ends without / i.e.: /prosperity/assistance-on-demand
AOD_HOST = {
    'PROTOCOL': "http",
    'IP': "localhost", 
    'PORT': 80,
    'PATH': ''
}
PREVIEW_SITE_URL = AOD_HOST['PATH']
ALLOWED_HOSTS = (
    '*',
)

#=================================
#   AOD ADMIN/MANAGER       
#=================================
ADMINS = (
    ('takis', DEVELOPER_EMAIL),
)
MANAGERS = ADMINS

#=================================
#   RDBMS CONFIGURATION     
#=================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aod',
        'USER': 'aod',
        'PASSWORD': 'aod',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8',
            'use_unicode': True, 
        },
    }
}

#==================================
#   APPLICATIONS MANAGEMENT      
#==================================
INSTALLED_APPS = (
    'statici18n',
    'modeltranslation',
    'colorful',
    #'compressor',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'restapi',
    'django_extensions',
    'debug_toolbar',
    'django_dowser',
    'rosetta',
    'grappelli',   
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'import_export',
    #'rosetta-grappelli',
    'rest_framework',
    'rest_framework_swagger',
    'drf_multiple_model',
    'analytical',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.sitemaps', 
    'robots',
    # 'constance',
)
