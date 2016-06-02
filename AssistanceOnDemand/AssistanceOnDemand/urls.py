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


# Uncomment the next lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Django rest framework views
from restapi import views as rviews, urls as rurls


urlpatterns = patterns('',

    ## Admin panel
    url(r'^grappelli/',                         include('grappelli.urls')), # grappelli URLS
    url(r'^admin/',                             include(admin.site.urls)),
    url(r'^admin/doc/',                         include('django.contrib.admindocs.urls')),

    # AoD app
    url(r'',                                    include(urls.patterns)),

    # AoD restapi
    url(r'^docs/',                              include('rest_framework_swagger.urls')),
    
    url(r'^api/v1/',                            include(rurls.endpoints,        namespace='aod_api')),
    url(r'^api-auth/',                          include('rest_framework.urls',  namespace='rest_framework')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# Debug static and media files via browser
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)



# HTTP status code
handler201 = 'app.views.created'
handler400 = 'app.views.bad_request'
handler401 = 'app.views.unauthorized'
handler403 = 'app.views.permission_denied'
handler404 = 'app.views.not_found'
handler405 = 'app.views.method_not_allowed'
handler415 = 'app.views.unsupported_media_type'
handler500 = 'app.views.server_error'


