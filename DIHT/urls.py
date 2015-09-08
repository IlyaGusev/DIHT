"""DIHT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

handler400 = 'DIHT.views.custom_400'
handler403 = 'DIHT.views.custom_403'
handler404 = 'DIHT.views.custom_404'
handler405 = 'DIHT.views.custom_405'
handler500 = 'DIHT.views.custom_500'
handler501 = 'DIHT.views.custom_501'
handler502 = 'DIHT.views.custom_502'
handler503 = 'DIHT.views.custom_503'

urlpatterns = [
    url(r'^', include('main.urls', namespace='main')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^washing/', include('washing.urls', namespace='washing')),
    url(r'^activism/', include('activism.urls', namespace='activism')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
