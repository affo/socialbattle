from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from socialbattle.public import views
router = SimpleRouter()

urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^rpg/dmg/$', views.get_damage)
)