"""tjadb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf             import settings
from django.conf.urls.static import static
from django.contrib          import admin
from django.urls             import path

import api.views     as api
import website.views as website

urlpatterns = [
    path('admin/',               admin.site.urls),

    path('api/artists' ,                api.artists),
    path('api/artist/<int:id>',         api.artist),
    path('api/charters',                api.charters),
    path('api/charter/<int:id>',        api.charter),
    path('api/browse',                  api.browse),
    path('api/browse_artist/<int:id>',  api.browse_artist),
    path('api/browse_charter/<int:id>', api.browse_charter),
    path('api/browse_source/<int:id>',  api.browse_source),
    path('api/sources',                 api.sources),
    path('api/source/<int:id>',         api.source),
    path('api/sotd',                    api.sotd),

    path('',                        website.index),
    path('artists/',                website.artists),
    path('charters/',               website.charters),
    path('sources/',                website.sources),
    path('browse/',                 website.browse),
    path('browse_artist/<int:id>',  website.browse_artist),
    path('browse_charter/<int:id>', website.browse_charter),
    path('browse_source/<int:id>',  website.browse_source),
    path('donate/',                 website.donate),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
