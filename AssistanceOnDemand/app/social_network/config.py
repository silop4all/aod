

SOCIAL_NETWORK_URL = "http://160.40.51.143:40000/aodsocial/app/#/home"
SOCIAL_NETWORK_WEB_SERVICES = {
    "url": "160.40.51.143:8080",
    "base": "http://160.40.51.143:8080",
    "services": {
        "insert": "/api/jsonws/aodsocial-portlet.aodsocial/on-register-aod-service/service-id/",
        "delete": "/api/jsonws/aodsocial-portlet.aodsocial/on-delete-aod-service/service-id/"
    },
    "users": {
        "insert": "/api/jsonws/aodsocial-portlet.aodsocial/login-with-register"
    },
    "sessions":{
        "logout": "/api/jsonws/aodsocial-portlet.aodsocial/propagate-logout/aod-user-id/"
    }
}
SOCIAL_NETWORK_WEB_SERVICES_AUTH = "anNvbndzOmxpZmVyYXk="