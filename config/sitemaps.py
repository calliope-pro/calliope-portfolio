from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url
from django.urls import reverse

from calliope_web.models import Bss

class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = 0.8

    def items(self):
        return [
            'calliope_web:home',
            'calliope_web:bss_list',
            'calliope_web:profile',
            'calliope_web:contact',
            'calliope_auth:login',
            'calliope_auth:signup',
            'calliope_web:support',
            'calliope_auth:logout',
            'calliope_auth:signup',
        ]
    
    def location(self, obj):
        return reverse(obj)
    

class BssSitemap(Sitemap):
    changefreq = "always"
    priority = 0.1
    def items(self):
        return Bss.objects.order_by('-updated_datetime')
    
    def location(self, obj):
        return reverse('calliope_web:bss_detail', kwargs={'pk':obj.pk})
    
    def lastmod(self, obj):
        return obj.updated_datetime


