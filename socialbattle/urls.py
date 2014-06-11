from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('socialbattle.api.urls')),
	url(r'^admin/', include(admin.site.urls)),
)

from socialbattle import settings
if not settings.DEBUG: #production
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	)