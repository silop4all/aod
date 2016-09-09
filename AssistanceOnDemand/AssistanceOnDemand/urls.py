"""
Definition of urls for AssistanceOnDemand.
"""

from django.conf import settings
from django.conf.urls.static import static

from datetime import datetime
from django.conf.urls import patterns, url, include
from app.forms import BootstrapAuthenticationForm
#import class
from app.views import * 
from app import urls

from django.conf.urls.i18n import i18n_patterns

# Uncomment the next lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Django rest framework views
from restapi import views as rviews, urls as rurls

prefix = settings.AOD_HOST['PATH'][1:]
if prefix != '':
    prefix += "/"

urlpatterns = patterns('',

    # Admin panel
    url(r'^' + str(prefix) + 'grappelli/',                         include('grappelli.urls')),                                     # grappelli URLS
    url(r'^' + str(prefix) + 'admin/',                             include(admin.site.urls)),
    url(r'^' + str(prefix) + 'admin/doc/',                         include('django.contrib.admindocs.urls')),

    #url(r'^' + str(prefix) + 'i18n/',                             include('django.conf.urls.i18n')),

    url(r'' + str(prefix) + '',                                     include(urls.patterns)),                                        # AoD app
    url(r'^' + str(prefix) + 'docs/',                              include('rest_framework_swagger.urls')),                        # AoD restapi
    url(r'^' + str(prefix) + 'api/v1/',                            include(rurls.endpoints,        namespace='private_api')),
    url(r'^' + str(prefix) + 'api-auth/',                          include('rest_framework.urls',  namespace='rest_framework')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^' + str(prefix) + 'admin/rosetta/', include('rosetta.urls')),
    )

if 'django_dowser' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^' + str(prefix) + 'admin/dowser/', include('django_dowser.urls')),
    )


#urlpatterns += i18n_patterns(
#    url(r'',                                    include(urls.patterns)),
#    url(r'^admin/',                             include(admin.site.urls)),
#    url(r'^admin/doc/',                         include('django.contrib.admindocs.urls')),
#    url(r'^docs/',                              include('rest_framework_swagger.urls')),
#    url(r'^api/v1/',                            include(rurls.endpoints,        namespace='aod_api')),
#    url(r'^api-auth/',                          include('rest_framework.urls',  namespace='rest_framework')),
#)

# Debug static and media files via browser
#if settings.DEBUG:
#    urlpatterns += patterns('',
#        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.MEDIA_ROOT,
#        }),
#        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.STATIC_ROOT,
#        }),
#)



# HTTP status code
handler201 = 'app.views.created'
handler400 = 'app.views.bad_request'
handler401 = 'app.views.unauthorized'
handler403 = 'app.views.permission_denied'
handler404 = 'app.views.not_found'
handler405 = 'app.views.method_not_allowed'
handler415 = 'app.views.unsupported_media_type'
handler500 = 'app.views.server_error'


