"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.sitemaps.views import sitemap, index

from . import sitemaps as sm
sitemaps = {
    'static': sm.StaticSitemap,
    'bss': sm.BssSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    path('', include('calliope_web.urls')),
    path('front/', include('calliope_front.urls', namespace='calliope_front')),
    path('auth/', include('calliope_auth.urls')),
    path('line-bot/', include('calliope_bot.urls')),
    path('api/v1/', include('api1.urls')),
]
