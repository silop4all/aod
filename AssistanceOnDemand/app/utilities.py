
from django.conf import settings
from django.core.mail import (
    EmailMultiAlternatives, 
    send_mail
)
from django.core.exceptions import ObjectDoesNotExist
from traceback import print_exc
from datetime import date
from app.models import Components

def sendEmail(receiversList, subject, content, includeHtml):
    try:
        sender = settings.EMAIL_HOST_USER
        format = "text/html"

        # send email with HTML code
        if includeHtml == True:
            msg = EmailMultiAlternatives(subject, "", sender, receiversList)
            msg.attach_alternative(content, format)
            msg.send()
        else:
            send_mail(subject, content, sender, receiversList, fail_silently=False)
    except:
        if settings.DEBUG:
            print_exc()
        pass


def domainURL():
    try:
        url = str(settings.AOD_HOST['PROTOCOL']) + "://" 
        url += str(settings.AOD_HOST['IP']) + ":" + str(settings.AOD_HOST['PORT'])
        return url
    except: 
        print_exc()
        pass


def get_version():
    # Write your own! That depends on your deployment strategy.
    # This example won't work if you release more than once a day.
    return date.today().isoformat()


def getTimeZone():
    return settings.TIME_ZONE


def getDistance(lat1, lon1, lat2, lon2):
    """
    Yield the linear distance among two points: user current point and the service's delivery point
    - A(lat1, lon1) -> user
    - B(lat2, lon2) -> service
    """
    
    try: 
        from math import sin, cos, pi, acos
        radlat1 = pi * lat1/180
        radlat2 = pi * lat2/180
        radlon1 = pi * lon1/180
        radlon2 = pi * lon2/180
        theta = lon1-lon2
        radtheta = pi * theta/180
        dist = sin(radlat1) * sin(radlat2) + cos(radlat1) * cos(radlat2) * cos(radtheta);
        dist = acos(dist)
        dist = dist * 180/pi
        dist = dist * 60 * 1.1515
        dist = dist * 1.609344
        return dist
    except: 
        print_exc()
        return -1



def socialNetworkIntegration():
    """
    Access database and decide if the "Social Network" is enabled in the AoD
    """
    try:
        soclialNetwork = Components.objects.get(name__exact="social_network")
        return soclialNetwork.is_enabled
    except ObjectDoesNotExist, e:
        if settings.DEBUG:
            print_exc()
        return -1
    except:
        print_exc()
        return -1


def AddToCartIntegration():
    """
    Access database and decide if the "Add To Cart" mechanism is enabled in the AoD
    """
    try:
        cart = Components.objects.get(name__exact="add_to_cart")
        return cart.is_enabled
    except ObjectDoesNotExist, e:
        if settings.DEBUG:
            print_exc()
        return -1
    except:
        return -1


def NewsletterIntegration():
    """
    Access database and decide if the "Newsletter" mechanism is enabled in the AoD
    """
    try:
        newsletter = Components.objects.get(name__exact="newsletter_banner")
        return newsletter.is_enabled
    except ObjectDoesNotExist, e:
        if settings.DEBUG:
            print_exc()
        return -1
    except:
        return -1


def compareLanguages(aliasList):
    """
    Retrieve the name of languages that are included in the aliasList
    """
    try:
        import pycountry
        languagesName = []
        
        for l in pycountry.languages:
            if l.terminology in aliasList:
                languagesName.append(l.name)
        return languagesName
    except:
        print_exc()
        return []
