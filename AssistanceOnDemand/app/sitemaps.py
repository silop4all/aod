# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap
from django.conf import settings
from django.core.urlresolvers import reverse
from app.models import Article



class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.modified_date

    def location(self, obj):
        return reverse('faq_article', kwargs= {'pk': obj.id})