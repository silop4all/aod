"""
Definition of urls for DjangoWebProject1.
"""

from django.conf import settings
from django.conf.urls.static import static

from datetime import datetime
from django.conf.urls import patterns, url, include
from app.forms import BootstrapAuthenticationForm
#import class
from app.views import * 


# Uncomment the next lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Django rest framework views
from restapi import views as rviews, urls as rurls



urlpatterns = patterns('',
    ##########################################
    ## Admin - default URLs
    ##########################################
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/',                     include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/',                         include(admin.site.urls)),


    # Visitors page
    url(r'^$',                              'app.views.home', name='home'),
    # login process - create session parameters [id, username]
    url(r'^login/$',                        'app.views.login', name='login'),
    url(r'^account/login/authorization/$',  'app.views.loginAuth'),
    # default logout process - delete session parameters
    url(r'^logout$',                        'django.contrib.auth.views.logout',{'next_page': '/',}, name='logout'),



    ##########################################
    ## Visitor registration/verification
    ##########################################
    url(r'^account/signup/$',               RegistrationView.as_view(), name='registration'),     # class-based view
    url(r'^account/signup/validation/$',    RegistrationView.as_view()),               # class-based view
    url(r'^account/signup-success/$',       'app.views.registrationSuccess'),             # function-based view
    url(r'^account/signup/username/$',      'app.views.usernameConstraints'),
    url(r'^account/signup/email/$',         'app.views.emailConstraints'),    
    url(r'^it-experience/$',                ItExperienceView.as_view()),                           # class-based view   
    url(r'^account/signup/countries/$',     CountriesView.as_view()),
    url(r'^account/signup/categories/$',    'app.views.categories'),
    # activate new account
    url(r'^account/activation$',            'app.views.accountActivation'),
    # Forgot pwd
    url(r'^account/forgot-password/$',      ForgotPasswordView.as_view(), name='forgotPassword'),


    # @TODO: check email of registered user -- use in registration from  => emailConstraints()
    url(r'^users/(?P<pk>\d+)$',             'app.views.checkEmail'), 

    ##########################################
    ## Dashboard - index
    ##########################################
    url(r'^index$',                         ServiceSearch.as_view(), name='home-page'),
    url(r'^services/search$',               ServiceSearchResults.as_view()),

    ##########################################
    ## Profile management
    ##########################################
    url(r'^profile/(?P<username>\w+)$',     'app.views.profile'),
    url(r'^profile/media/(?P<pk>\d+)$',     UploadUserMedia.as_view()),            # cover image
    url(r'^profile/personal/(?P<pk>\d+)$',  UserUpdatePersonalInfo.as_view()),       # personal info
    url(r'^profile/contact/(?P<pk>\d+)$',   UserUpdateContactInfo.as_view()),         # contact info
    url(r'^profile/platform/(?P<pk>\d+)$',  UserUpdatePlatformInfo.as_view()),       # platform settings
    #url(r'^profile/bank-settings/(?P<pk>\d+)$', 'app.views.updateBankSettings'),   # bank info - TODO in future

    ##########################################
    ## Services
    ##########################################
    # Index services of provider
    url(r'^provider$',                                      ServicesIndex.as_view()),
    # Create new service
    url(r'^provider/services$',                             ServiceCreate.as_view()),
    # Preview/Update/Delete service
    url(r'^provider/services/(?P<alias>[^/]+)/$',           ServiceView.as_view()),
    # Update service
    url(r'^provider/services/(?P<alias>[^/]+)/modify/$',    ServiceUpdateView.as_view()),
    # upload service media (cover/image/package)
    url(r'^provider/services/media/upload/(?P<pk>\d+)$',    UploadServiceMedia.as_view()),

    ##########################################
    ## Services - consumers views
    ##########################################
    url(r'^services/(?P<alias>[^/]+)/$',                    ServiceConsumerView.as_view()),

    ##########################################
    ## AoD technical support
    ##########################################
    # index page
    url(r'^support$',                               TechnicalSupport.as_view()),
    url(r'^support/create-new-account$',            CreateAccountSupport.as_view()),
    url(r'^support/log-in-out$',                    LogInOutSupport.as_view(), name='log-in-out'),
    url(r'^support/forget-password',                ForgetPasswordSupport.as_view(), name='forget_password'),
    url(r'^support/update-profile-steps',           UpdateProfileSupport.as_view()),
    url(r'^support/change-my-password',             ChangePasswordSupport.as_view()),
    # provider 
    url(r'^support/services/register',              RegisterServiceSupport.as_view()),
    url(r'^support/services/update',                UpdateServiceSupport.as_view()),
    url(r'^support/services/delete',                DeleteServiceSupport.as_view()),



    ##########################################
    ## Add to card
    ##########################################
    url(r'^cart/preview', CartView.as_view()),
    url(r'^cart/update/(?P<service_pk>\d+)$',       CartView.as_view()),
    url(r'^cart/delete/(?P<service_pk>\d+)$',       CartView.as_view()),


    ##########################################
    ## Consumer stats
    ##########################################
     url(r'^my-statistics/preview$',                MyStats.as_view()),   


    ###########################################
    ##  NAS component urls
    ###########################################
    url(r'^network-assistance-services/requests$',                          NetworkAssistanceServicesRequests.as_view(),        name='carer-landing-page'),
    url(r'^network-assistance-services/requests/search$',                   NetworkAssistanceServicesFindUsers.as_view()),
    url(r'^network-assistance-services/requests/create-new$',               NetworkAssistanceServicesCreateRequest.as_view()),
    url(r'^network-assistance-services/requests/reply$',                    NetworkAssistanceServicesReplyRequest.as_view()),
    url(r'^network-assistance-services/requests/(?P<pk>\d+)$',              NetworkAssistanceServices.as_view()),
    
    url(r'^network-assistance-services/configuration/(?P<consumer>\d+)',    NetworkAssistanceServicesConfiguration.as_view()),
    url(r'^network-assistance-services/services/search$',                   SearchNetworkAssistanceServices.as_view()),
    url(r'^network-assistance-services/services/temporal-setup$',           NetworkAssistanceServicesQueue.as_view()),
    url(r'^network-assistance-services/services/submit',                    NetworkAssistanceServicesSubmit.as_view()),
    url(r'^network-assistance-services/services/search/keywords$',          SearchKwdNetworkAssistanceServices.as_view()),
    url(r'^network-assistance-services/services/preview/(?P<consumer>\d+)$',PreviewNetworkAssistanceServices.as_view()),
    
    url(r'^network-assistance-services/services/(?P<pk>\d+)/configuration$',ServiceConfigurationView.as_view()),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + rurls.endpoints



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


