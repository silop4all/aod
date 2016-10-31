# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils import translation


class SyncLanguageCookie(object):
    """Sync the user preferred language 
        Detect if different exists among COOKIE language code and url language code
    """

    def process_response(self, request, response):
        try:
            # if language CODE in URL is different from COOKIE code, sync them
            url_lang_code = translation.get_language()
            cookie_lang_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME) 
            
            if url_lang_code != cookie_lang_code:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, url_lang_code)
            return response
        except Exception, ex:
            if settings.DEBUG:
                print "[ERROR] " + str(ex)
            return response