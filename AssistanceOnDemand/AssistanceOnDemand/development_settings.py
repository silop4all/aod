# -*- coding: utf-8 -*-

"""
Settings for development purposes

TO BE DEFINED:
    DEVELOPER_EMAIL
    AOD_HOST
    DATABASES
"""

#=================================
#   DEBUG SETTINGS     
#=================================
DEBUG = True

#=================================
#   EVALUATION CONTACT     
#=================================
EVALUATION_PROCESS  = False
DEVELOPER_EMAIL = 'pathanasoulis@ep.singularlogic.eu'
EVALUATOR_EMAIL = DEVELOPER_EMAIL
RECEIVER_EMAIL = [EVALUATOR_EMAIL]

#=================================
#   AOD HOST INFO           
#=================================
AOD_HOST = {
    'PROTOCOL': "http",
    'IP': "192.168.1.47", 
    'PORT': 8000,
    'PATH': ''
}
PREVIEW_SITE_URL = AOD_HOST['PATH']
ALLOWED_HOSTS = (
    'localhost',
    '*'
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
        'NAME': 'pros4all',
        'USER': 'root',
        'PASSWORD': '',
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
    #'rosetta-grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'import_export',
    'rest_framework',
    'rest_framework_swagger',
    'analytical',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.sitemaps', 
    'robots'
    # 'constance',
)
