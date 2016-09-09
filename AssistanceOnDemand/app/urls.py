from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse
from django.conf import settings
from app.views import * 

AOD_ROOT = settings.AOD_HOST['PATH'] if len(settings.AOD_HOST['PATH']) > 1 and settings.AOD_HOST['PATH'][0] == "/" else settings.AOD_HOST['PATH'] + "/"


if settings.OPENAM_INTEGRATION:
    access = patterns('',

        url(r'^login/$',                                                Oauth2Login.as_view(),                              name='login_page'),
        url(r'^account/signup/$',                                       Oauth2SignUp.as_view(),                             name='registration_page'),
        url(r'^logout/$',                                               Logout.as_view(),                                   name='logout'),
    )
else:
    access = patterns('',

        url(r'^login/$',                                                'app.views.login',                                  name='login_page'),
        url(r'^account/login/authorization/$',                          'app.views.loginAuth',                              name='login-authorization'),
        url(r'^logout/$',                                               'django.contrib.auth.views.logout',{'next_page': AOD_ROOT,},   name='logout'),

        ##########################################
        ## Visitor registration/verification
        ##########################################
        url(r'^account/signup/$',                       RegistrationView.as_view(),         name='registration_page'), 
        url(r'^account/signup/validation/$',            RegistrationView.as_view(),         name='validate-registration'),
        url(r'^account/signup-success/$',                               'app.views.registrationSuccess',                    name='account_success_registration'),
        url(r'^account/signup/username/$',              'app.views.usernameConstraints',    ),
        url(r'^account/signup/email/$',                 'app.views.emailConstraints',       ),
        url(r'^account/signup/countries/$',             CountriesView.as_view(),            ),
        url(r'^account/signup/categories/$',            'app.views.categories',             ),
        # activate new account
        url(r'^account/activation$',                                    'app.views.accountActivation',                      name="account_activation"),
        # Forgot pwd
        url(r'^account/forgot-password/$',              ForgotPasswordView.as_view(), name='forgotPassword'),
    )



patterns = patterns('',

    url(r'^$',                                                      'app.views.home',                                   name='landing_page'),

    url(r'^it-experience/$',                                        ItExperienceView.as_view(),                         name="it_familiarity"),

    ##########################################
    ## Profile management
    ##########################################
    url(r'^profile/(?P<username>\w+)$',                             'app.views.profile',                                name="user_profile"), 
    url(r'^profile/media/(?P<pk>\d+)$',                             UploadUserMedia.as_view(),                          name="profile_media"), 
    url(r'^profile/personal/(?P<pk>\d+)$',                          UserUpdatePersonalInfo.as_view(),                   name="personal_profile_update"), 
    url(r'^profile/contact/(?P<pk>\d+)$',                           UserUpdateContactInfo.as_view(),                    name="contact_profile_update"), 
    url(r'^profile/platform/(?P<pk>\d+)$',                          UserUpdatePlatformInfo.as_view(),                   name="platform_profile_update"), 
    url(r'^users/(?P<pk>\d+)$',                                     'app.views.checkEmail',                             name="validate_profile_field"), 

    ##########################################
    ## Dashboard - index
    ##########################################
    url(r'^index/$',                                                ServiceSearch.as_view(),                            name='home_page'),
    url(r'^services/search/$',                                      ServiceSearchResults.as_view(),                     name="search_services"),
    ##########################################
    ## Services - consumers views
    ##########################################
    url(r'^services/(?P<alias>[^/]+)/$',                            ServiceConsumerView.as_view(),                      name="service_view_page"),
    ##########################################
    ## Services -> Offerings
    ##########################################
    # Index services of provider
    url(r'^offerings/$',                                            ServicesIndex.as_view(),                            name='provider_dashboard'),
    # Create new service
    url(r'^offerings/services/$',                                   ServiceCreate.as_view(),                            name='insert_service'),
    # Preview/Update/Delete service
    url(r'^offerings/services/(?P<alias>[^/]+)/$',                  ServiceView.as_view(),                              name='public_service_view'),
    # Update service @fix
    url(r'^offerings/services/(?P<alias>[^/]+)/modify/$',           ServiceUpdateView.as_view(),                        name='update_service'),
    # upload service media (cover/image/package)
    url(r'^offerings/services/media/upload/(?P<pk>\d+)$',           UploadServiceMedia.as_view(),                       name='upload_service_media'),
    ##########################################
    ## Consumer stats
    ##########################################
    url(r'^collection/$',                                           MyStats.as_view(),                                  name='consumer_dashboard'),
    ##########################################
    ## Add to card
    ##########################################
    url(r'^cart/preview/$',                                         CartView.as_view(),                                 name='cart_preview'),
    url(r'^cart/update/(?P<service_pk>\d+)$',                       CartView.as_view(),                                 name="add_item_cart"),
    url(r'^cart/delete/(?P<service_pk>\d+)$',                       CartView.as_view(),                                 name="remove_item_cart"),
    ##########################################
    ## AoD technical support
    ##########################################
    url(r'^support/$',                                              TechnicalSupport.as_view(),                         name='platform_technical_support_page'),
    url(r'^support/create-new-account/$',                           CreateAccountSupport.as_view(),                     name="create_aod_account_guide"),
    url(r'^support/access-issues/$',                                LogInOutSupport.as_view(),                          name='log_in_out_guide'),
    url(r'^support/forget-password/$',                              ForgetPasswordSupport.as_view(),                    name='reset_password_guide'),
    url(r'^support/update-my-profile/$',                            UpdateProfileSupport.as_view(),                     name="update_profile_guide"),
    url(r'^support/change-my-password/$',                           ChangePasswordSupport.as_view(),                    name="change_password_guide"),
    url(r'^support/register-a-service/$',                           RegisterServiceSupport.as_view(),                   name="register_service_guide"),
    url(r'^support/update-a-service/$',                             UpdateServiceSupport.as_view(),                     name="update_service_guide"),
    url(r'^support/remove-a-service/$',                             DeleteServiceSupport.as_view(),                     name="remove_service_guide"),
    ###########################################
    ##  Assistance urls
    ###########################################
    url(r'^guided-assistance/$',                                    NetworkAssistanceServicesRequests.as_view(),        name='guided_assistance_landing_page'),
    url(r'^guided-assistance/requests/$',                           NetworkAssistanceServicesCreateRequest.as_view(),   name='guided_assistance_carer_request'),
    url(r'^guided-assistance/requests/(?P<pk>\d+)$',                NetworkAssistanceServices.as_view(),                name="guided_assistance_request"),
    url(r'^guided-assistance/requests/search$',                     NetworkAssistanceServicesFindUsers.as_view(),       name='guided_assistance_consumer_search'),
    url(r'^guided-assistance/requests/reply$',                      NetworkAssistanceServicesReplyRequest.as_view(),    name="guided_assistance_reply_to_request"),
    url(r'^guided-assistance/invitations/$',                        NetworkAssistanceServicesInviteCarers.as_view(),    name='guided_assistance_consumer_invitation'),
    url(r'^guided-assistance/invitations/reply$',                   NetworkAssistanceServicesCarerReply.as_view(),      name='guided_assistance_reply_consumer_invitation'),
    url(r'^guided-assistance/configuration/(?P<consumer>\d+)$',     NetworkAssistanceServicesConfiguration.as_view(),   name="guided_assistance_network_setup"),
    url(r'^guided-assistance/services/search$',                     SearchNetworkAssistanceServices.as_view(),          name="guided_assistance_retrieve_services"),
    url(r'^guided-assistance/services/temporal-setup$',             NetworkAssistanceServicesQueue.as_view(),           name="guided_assistance_temp_services"),
    url(r'^guided-assistance/services/submit$',                     NetworkAssistanceServicesSubmit.as_view(),          name="guided_assistance_submit_services"),
    url(r'^guided-assistance/services/search/keywords$',            SearchKwdNetworkAssistanceServices.as_view(),       name="guided_assistance_search_by_keywords"),
    url(r'^guided-assistance/services/preview/(?P<consumer>\d+)/$', PreviewNetworkAssistanceServices.as_view(),         name="guided_assistance_network_preview"),


    url(r'^assistance/services/(?P<pk>\d+)/configuration$',     ServiceConfigurationView.as_view()),

    #test
    url(r'^callback/openam$',                                       Callback.as_view({"get": "retrieve"}),              name='callback_url'), 

) + access