
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from traceback import print_exc

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


