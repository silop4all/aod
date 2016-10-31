"""
Definition of urls for AssistanceOnDemand.
"""

from django.conf import settings
from django.conf.urls.static import static

from datetime import datetime
from django.conf.urls import patterns, url, include
#import class
from app.views import * 
from app import urls

from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import javascript_catalog


# Uncomment the next lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from filebrowser.sites import site

from django.contrib.sitemaps.views import sitemap
from app.sitemaps import ArticleSitemap


# Django rest framework views
from restapi import views as rviews, urls as rurls

prefix = settings.AOD_HOST['PATH'][1:]
if prefix != '':
    prefix += "/"

js_info_dict = {
    'packages': ('app',)
}


sitemaps = {
    "app": ArticleSitemap,
}


urlpatterns = patterns('',

    # Admin panel
    url(r'^' + str(prefix) + 'admin/filebrowser/',                  include(site.urls)),
    url(r'^' + str(prefix) + 'grappelli/',                          include('grappelli.urls')),                                     # grappelli URLS
    url(r'^' + str(prefix) + 'admin/',                              include(admin.site.urls)),
    url(r'^' + str(prefix) + 'admin/doc/',                          include('django.contrib.admindocs.urls')),

    url(r'^' + str(prefix) + 'i18n/',                               include('django.conf.urls.i18n')),

    url(r'' + str(prefix) + '',                                     include(urls.patterns)),                                        # AoD app
    url(r'^' + str(prefix) + 'docs/',                               include('rest_framework_swagger.urls')),                        # AoD restapi
    url(r'^' + str(prefix) + 'api/v1/',                             include(rurls.endpoints,        namespace='private_api')),
    url(r'^' + str(prefix) + 'api-auth/',                           include('rest_framework.urls',  namespace='rest_framework')),

    url(r'^' + str(prefix) + 'admin/rosetta/',                      include('rosetta.urls')),
    url(r'^' + str(prefix) + 'admin/dowser/',                       include('django_dowser.urls')),

    url(r'^' + str(prefix) + 'ckeditor/',                           include('ckeditor_uploader.urls')),

    url(r'^' + str(prefix) + 'sitemap\.xml$',                       sitemap, {'sitemaps': sitemaps},    name='django.contrib.sitemaps.views.sitemap'),
    url(r'^' + str(prefix) + 'robots.txt$',                         include('robots.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = i18n_patterns(
    url(r'' + str(prefix) + '',                                     include(urls.patterns)),
    url(r'^' + str(prefix) + 'admin/filebrowser/',                  include(site.urls)),
    url(r'^' + str(prefix) + 'i18n/',                               include('django.conf.urls.i18n')),
    url(r'^' + str(prefix) + 'grappelli/',                          include('grappelli.urls')),                                     # grappelli urls
    url(r'^' + str(prefix) + 'admin/',                              include(admin.site.urls)),
    url(r'^' + str(prefix) + 'admin/doc/',                          include('django.contrib.admindocs.urls')),
    url(r'^' + str(prefix) + 'docs/',                               include('rest_framework_swagger.urls')),
    url(r'^' + str(prefix) + 'api/v1/',                             include(rurls.endpoints,        namespace='private_api')),
    url(r'^' + str(prefix) + 'api-auth/',                           include('rest_framework.urls',  namespace='rest_framework')),

    url(r'^' + str(prefix) + 'admin/rosetta/',                      include('rosetta.urls')),
    url(r'^' + str(prefix) + 'admin/dowser/',                       include('django_dowser.urls')),

    url(r'^' + str(prefix) + 'ckeditor/',                           include('ckeditor_uploader.urls')),

    url(r'^' + str(prefix) + 'sitemap\.xml$',                       sitemap, {'sitemaps': sitemaps},    name='django.contrib.sitemaps.views.sitemap'),
    url(r'^' + str(prefix) + 'robots.txt$',                         include('robots.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug static and media files via browser
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^' + str(prefix) + 'media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^' + str(prefix) + 'static/(?P<path>.*)$', 'django.views.static.serve', {
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


