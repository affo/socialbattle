from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
import views

user_urls = patterns('',
	url(r'^(?P<username>[0-9a-zA-Z_-]+)/characters$', views.UserCharacterList.as_view(), name='usercharacter-list'),
	url(r'^(?P<username>[0-9a-zA-Z_-]+)$', views.UserDetail.as_view(), name='user-detail'),
	url(r'^$', views.UserList.as_view(), name='user-list')
)

character_urls = patterns('',
	url(r'^(?P<pk>\d+)$', views.CharacterDetail.as_view(), name='character-detail'),
	url(r'^$', views.CharacterList.as_view(), name='character-list')
)

urlpatterns = patterns('',
	url(r'^users/', include(user_urls)),
	url(r'^character/', include(character_urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns)