from django.conf.urls import patterns, url, include
from app.views import * 



patterns = patterns('',

    # Visitors page
    url(r'^$',                                      'app.views.home',       name='home'),
    url(r'^login/$',                                'app.views.login',      name='login'),
    url(r'^account/login/authorization/$',          'app.views.loginAuth',  name='login-authorization'),
    url(r'^logout$',                                'django.contrib.auth.views.logout',{'next_page': '/',}, name='logout'),



    ##########################################
    ## Visitor registration/verification
    ##########################################
    url(r'^account/signup/$',                       RegistrationView.as_view(),         name='registration'), 
    url(r'^account/signup/validation/$',            RegistrationView.as_view(),         name='validate-registration'),
    url(r'^account/signup-success/$',               'app.views.registrationSuccess',    name='success-registration'),
    url(r'^account/signup/username/$',              'app.views.usernameConstraints',    ),
    url(r'^account/signup/email/$',                 'app.views.emailConstraints',       ),
    url(r'^it-experience/$',                        ItExperienceView.as_view(),         ),
    url(r'^account/signup/countries/$',             CountriesView.as_view(),            ),
    url(r'^account/signup/categories/$',            'app.views.categories',             ),
    # activate new account
    url(r'^account/activation$',                    'app.views.accountActivation'),
    # Forgot pwd
    url(r'^account/forgot-password/$',              ForgotPasswordView.as_view(), name='forgotPassword'),


    # @TODO: check email of registered user -- use in registration from  => emailConstraints()
    url(r'^users/(?P<pk>\d+)$',                     'app.views.checkEmail'), 

    ##########################################
    ## Dashboard - index
    ##########################################
    url(r'^index$',                                 ServiceSearch.as_view(), name='home-page'),
    url(r'^services/search$',                       ServiceSearchResults.as_view()),

    ##########################################
    ## Profile management
    ##########################################
    url(r'^profile/(?P<username>\w+)$',             'app.views.profile'),
    url(r'^profile/media/(?P<pk>\d+)$',             UploadUserMedia.as_view()),            # cover image
    url(r'^profile/personal/(?P<pk>\d+)$',          UserUpdatePersonalInfo.as_view()),       # personal info
    url(r'^profile/contact/(?P<pk>\d+)$',           UserUpdateContactInfo.as_view()),         # contact info
    url(r'^profile/platform/(?P<pk>\d+)$',          UserUpdatePlatformInfo.as_view()),       # platform settings

    ##########################################
    ## Services -> Offerings
    ##########################################
    # Index services of provider
    url(r'^offerings$',                                      ServicesIndex.as_view(),       name='provider-dashboard'),
    # Create new service
    url(r'^offerings/services$',                             ServiceCreate.as_view(),       name='insert_service'),
    # Preview/Update/Delete service
    url(r'^offerings/services/(?P<alias>[^/]+)/$',           ServiceView.as_view(),         name='public_service_view'),
    # Update service @fix
    url(r'^offerings/services/(?P<alias>[^/]+)/modify/$',    ServiceUpdateView.as_view(),   name='update_service'),
    # upload service media (cover/image/package)
    url(r'^offerings/services/media/upload/(?P<pk>\d+)$',    UploadServiceMedia.as_view(),  name='upload_service_media'),

    ##########################################
    ## Services - consumers views
    ##########################################
    url(r'^services/(?P<alias>[^/]+)/$',                    ServiceConsumerView.as_view()),

    ##########################################
    ## AoD technical support
    ##########################################
    # index page
    url(r'^support$',                               TechnicalSupport.as_view(),         name='help'),
    url(r'^support/create-new-account$',            CreateAccountSupport.as_view()),
    url(r'^support/log-in-out$',                    LogInOutSupport.as_view(),          name='log-in-out'),
    url(r'^support/forget-password',                ForgetPasswordSupport.as_view(),    name='forget_password'),
    url(r'^support/update-profile-steps',           UpdateProfileSupport.as_view()),
    url(r'^support/change-my-password',             ChangePasswordSupport.as_view()),
    # provider 
    url(r'^support/services/register',              RegisterServiceSupport.as_view()),
    url(r'^support/services/update',                UpdateServiceSupport.as_view()),
    url(r'^support/services/delete',                DeleteServiceSupport.as_view()),



    ##########################################
    ## Add to card
    ##########################################
    url(r'^cart/preview',                           CartView.as_view(),         name='cart'),
    url(r'^cart/update/(?P<service_pk>\d+)$',       CartView.as_view()),
    url(r'^cart/delete/(?P<service_pk>\d+)$',       CartView.as_view()),


    ##########################################
    ## Consumer stats
    ##########################################
    #url(r'^my-statistics/preview$',                MyStats.as_view(),          name='consumer-dashboard'),
    url(r'^collection/preview$',                    MyStats.as_view(),          name='consumer-dashboard'),


    ###########################################
    ##  Assistance urls
    ###########################################
    url(r'^assistance/requests$',                               NetworkAssistanceServicesRequests.as_view(),        name='carer-landing-page'),
    url(r'^assistance/requests/search$',                        NetworkAssistanceServicesFindUsers.as_view(),       name='carer-search-consumer'),
    url(r'^assistance/requests/send$',                          NetworkAssistanceServicesCreateRequest.as_view(),   name='carer-find-enduser'),
    url(r'^assistance/requests/reply$',                         NetworkAssistanceServicesReplyRequest.as_view()),
    url(r'^assistance/requests/(?P<pk>\d+)$',                   NetworkAssistanceServices.as_view()),
    url(r'^assistance/invitations$',                            NetworkAssistanceServicesInviteCarers.as_view(),    name='consumer_invite_carer'),
    url(r'^assistance/invitations/reply$',                      NetworkAssistanceServicesCarerReply.as_view(),      name='carer_reply_invitation'),

    url(r'^assistance/configuration/(?P<consumer>\d+)',         NetworkAssistanceServicesConfiguration.as_view()),
    url(r'^assistance/services/search$',                        SearchNetworkAssistanceServices.as_view()),
    url(r'^assistance/services/temporal-setup$',                NetworkAssistanceServicesQueue.as_view()),
    url(r'^assistance/services/submit',                         NetworkAssistanceServicesSubmit.as_view()),
    url(r'^assistance/services/search/keywords$',               SearchKwdNetworkAssistanceServices.as_view()),
    url(r'^assistance/services/preview/(?P<consumer>\d+)$',     PreviewNetworkAssistanceServices.as_view()),
    url(r'^assistance/services/(?P<pk>\d+)/configuration$',     ServiceConfigurationView.as_view()),
)