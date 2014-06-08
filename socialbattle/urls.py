from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('socialbattle.api.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)
