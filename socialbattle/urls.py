from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^api/', include('socialbattle.api.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
)
