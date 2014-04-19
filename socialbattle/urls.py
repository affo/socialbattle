from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from apps.api.views import root, api_root, UserViewSet

from django.contrib import admin
admin.autodiscover()

router = SimpleRouter()
#router.register(r'api/words', WordViewSet)
router.register(r'api/users', UserViewSet)

urlpatterns = patterns('',
	#this url returns the web page
	url(r'^api/$', api_root),
	url(r'^$', root),

	url(r'^', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^facebook/', include('django_facebook.urls')),
	url(r'^accounts/', include('django_facebook.auth_urls')),
)

urlpatterns = format_suffix_patterns(urlpatterns)
