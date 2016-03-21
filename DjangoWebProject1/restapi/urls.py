from django.conf.urls import patterns, url, include
from restapi import views as rviews

endpoints = patterns('',

    # swagger
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # REST endpoints
    url(r'^api-auth/',                      include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/v1/it_experiences$',         rviews.ItExperienceList.as_view()),
    url(r'^api/v1/members',                 rviews.UsersList.as_view()),

    url(r'^api/v1/tags',                    rviews.TagList.as_view()),
    url(r'^api/v1/categories$',             rviews.CategoriesList.as_view()),
    url(r'^api/v1/categories/(?P<pk>\d+)$', rviews.CategoriesResource.as_view()),
    url(r'^api/v1/services$',               rviews.ServicesList.as_view()),
    url(r'^api/v1/services/(?P<pk>\d+)$',   rviews.ServicesResource.as_view()),
 
    url(r'^api/v1/charging_policies$',      rviews.ChargingPoliciesList.as_view()),
    url(r'^api/v1/guided_networks',         rviews.CarerAssistConsumerList.as_view()),

)