from django.conf.urls import patterns, url, include
from restapi import views as rviews

endpoints = patterns(
    '',
    #url(r'members',                                 rviews.UsersList.as_view()),

    url(r'^skills$',                                 rviews.ItExperienceList.as_view()),
    url(r'^charging_policies$',                      rviews.ChargingPoliciesList.as_view()),

    url(r'^categories$',                             rviews.CategoriesList.as_view()),
    url(r'^categories/tree$',                        rviews.TreeCategoriesList.as_view(),               name="categories_tree"),
    url(r'^categories/(?P<pk>\d+)$',                 rviews.CategoriesResource.as_view()),
    url(r'^tags$',                                   rviews.TagList.as_view()),
      
    url(r'^services$',                               rviews.ServicesList.as_view()),
    url(r'^services/(?P<pk>\d+)$',                   rviews.ServicesResource.as_view(),                 name="service_entity"),
    url(r'^services/(?P<pk>\d+)/keywords$',          rviews.ServiceKeywordsList.as_view(),              name="service_keywords"),
    url(r'^services/(?P<pk>\d+)/configuration$',     rviews.ServiceConfigList.as_view(),                name="service_configuration"),
    url(r'^services/(?P<service>\d+)/reviews$',      rviews.ServiceReviewsList.as_view(),               name="service_reviews"),
    url(r'^services/(?P<pk>\d+)/details$',           rviews.DetailedServiceResource.as_view(),          name="detailed_service"),
    url(r'^services/(?P<pk>\d+)/languages$',         rviews.ServiceLanguagesList.as_view(),             name="service_languages"),

    url(r'^services/(?P<pk>\d+)/technical-materials$',  rviews.ServiceMaterialsList.as_view(),          name="service_technical_support"),
    url(r'^technical-materials/(?P<pk>\d+)$',           rviews.ServiceMaterialResource.as_view(),       name="technical_material"),


    
    url(r'^languages$',                             rviews.SupportedLanguagesResource.as_view(),        name='service-languages'),

    url(r'^consumers/(?P<pk>\d+)/services$',        rviews.ConsumerServicesList.as_view(),              name='consumer_services'),
    



    # assist
    url(r'^assistance/configuration$',               rviews.AssistanceConfigurationList.as_view(),      name="service_consumer_configuration"),
    url(r'^assistance/consumers/(?P<pk>\d+)/services$',  rviews.ConsumerAssistServicesList.as_view(),   name='assist_consumer_services'),
    url(r'^assistance/consumers/(?P<pk>\d+)/services/(?P<service>\d+)/configuration$',  rviews.ConsumerAssistServicesConfigurationList.as_view(),  name='assist_consumer_service_config'),

    url(r'^assistance/carers$',                     rviews.UserRolesList.as_view(),                     name='carers_list'),

    # fix or deprecate them
    #url(r'configuration/(?P<pk>\d+)$',              rviews.ServiceConfigurationList.as_view()),    
    

    url(r'^support/questions',                      rviews.PublishQuestionList.as_view(),               name="support_questions")
)