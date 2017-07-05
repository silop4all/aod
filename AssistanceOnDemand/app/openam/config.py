# -*- coding: utf-8 -*-

from django.conf import settings


base_url = settings.OAUTH_SERVER

__openam__ = {
    "base": "http://" + str(base_url),
    "endpoints": {
        "access_token": "/openam/oauth2/access_token",
        "check_access_token": "/openam/oauth2/tokeninfo",
        "basic_profile": '/openam/oauth2/userinfo'
    }
}

__iam__ = {
    "base": "http://" + str(base_url),
    "endpoints": {
        "authorize": "/prosperity4all/identity-access-manager/oauth2/authorize/",
        "signup": "/prosperity4all/identity-access-manager/signup-request/",
        "full_profile": "/prosperity4all/identity-access-manager/api/oauth2/userinfo",
        "roles": "/prosperity4all/identity-access-manager/api/oauth2/roles",
    }
}

