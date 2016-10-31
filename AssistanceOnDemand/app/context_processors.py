# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils import translation
from traceback import print_exc
from app.models import (
    Logo,
    Favicon,
    Components,
    SocialNetwork,
    LanguageFlag,
    Theme,
    UserTheme,
    Metadata,
    Topic,
)

def app_processor(request):
    """
    Return global variables for the app application
    
    For example return the app's logo information and links in social media.
    """

    bootstrap_table_locale_url = {
        'en': 'bootstrap-table-en-US.min.js',
        'el': 'bootstrap-table-el-GR.min.js',
        'es': 'bootstrap-table-es-SP.min.js',
        'fr': 'bootstrap-table-fr-FR.min.js',
        'it': 'bootstrap-table-it-IT.min.js',
        'de': 'bootstrap-table-de-DE.min.js',
    }

    try:
        logo = Logo.objects.get(selected=True)
    except:
        logo = {"title": "select_logo"}

    try:
        favicon = Favicon.objects.get(selected=True)
    except:
        favicon = {"title": "AoD"}

    try:
        if 'id' in request.session.keys():
            user_id = request.session['id']
            preference  = UserTheme.objects.get(user_id__exact=user_id)
        else:
            cookie_theme = request.COOKIES.get(settings.THEME_COOKIE_NAME)
            preference  = UserTheme.objects.get(theme_id__exact=cookie_theme)
        theme = Theme.objects.get(pk=preference.theme_id)
    except:
        theme = Theme.objects.get(is_default=True)

    try:
        metadata = Metadata.objects.get(active=True)
    except:
        metadata = {}

    components = dict()
    try:
        for k,v in Components.objects.all().values_list('name', 'is_enabled').distinct():
            components[k] = v
    except:     
       print_exc()

    return {
        'logo': logo,
        'favicon': favicon,
        'components': components,
        'social_networks': SocialNetwork.objects.filter(visible=True),
        'topics': Topic.objects.filter(visible=True).values('id', 'title'),
        'flags': [{"code":v[0], "name":v[1], "flag": LanguageFlag.objects.get(alias__iexact=v[0]).flag} for i,v in enumerate(settings.LANGUAGES)],
        'theme':  {"url": "" + str(theme.url), "title": theme.title },
        'metadata': metadata,
        'bootstrap_table_locale_url': bootstrap_table_locale_url[str(translation.get_language())],
        'username': request.session["username"] if "username" in request.session else None,
        "google_maps_key": settings.GOOGLE_MAPS_KEY,
    }


