from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
import views

signx_urls = patterns('',
	url(r'^up/$', views.signup, name='signup'),
	url(r'^in/$', 'rest_framework.authtoken.views.obtain_auth_token', name='signin'),
	url(r'^out/$', views.signout, name='signout'),
)

follow_view = views.FollowView.as_view({
	'get': 'followx',
})
user_urls = patterns('',
	url(r'^(?P<username>[0-9a-zA-Z_-]+)/characters/$', views.UserCharacterList.as_view(), name='usercharacter-list'),
	url(r'^(?P<username>[0-9a-zA-Z_-]+)/$', views.UserDetail.as_view(), name='user-detail'),
	url(r'^$', views.UserList.as_view(), name='user-list'),

	url(r'^(?P<username>[0-9a-zA-Z_-]+)/follow(?P<direction>[0-9a-zA-Z_-]+)/$', follow_view, name='followx-list'),
)

search_urls = patterns('',
	url(r'^users/$', views.search_user, name='user-search'),
	url(r'^characters/$', views.search_character, name='character-search'),
	url(r'^rooms/$', views.search_room, name='room-search'),
)

character_urls = patterns('',
	url(r'^(?P<name>[0-9a-zA-Z_-]+)/$', views.CharacterDetail.as_view(), name='character-detail'),
	url(r'^$', views.CharacterList.as_view(), name='character-list'),
)

room_urls = patterns('',
	#url(r'^relax/$', views.RelaxRoomList.as_view(), name='relaxroom-list'),
	url(r'^pve/$', views.PVERoomList.as_view(), name='pveroom-list'),
	url(r'^relax/(?P<name>[0-9a-zA-Z_-]+)/$', views.RelaxRoomDetail.as_view(), name='relaxroom-detail'),
	url(r'^pve/(?P<name>[0-9a-zA-Z_-]+)/$', views.PVERoomDetail.as_view(), name='pveroom-detail'),
	url(r'^$', views.RoomList.as_view(), name='room-list'),
)

mob_urls = patterns('',
	url(r'^(?P<name>[0-9a-zA-Z_-]+)/$', views.MobDetail.as_view(), name='mob-detail'),
)

item_urls = patterns('',
	url(r'^(?P<pk>[0-9a-zA-Z_-]+)/$', views.ItemDetail.as_view(), name='item-detail'),
)

urlpatterns = patterns('',
	url(r'^$', views.api_root, name='api-root'),
	url(r'^users/', include(user_urls)),
	url(r'^characters/', include(character_urls)),
	url(r'^rooms/', include(room_urls)),
	url(r'^mobs/', include(mob_urls)),
	url(r'^items/', include(item_urls)),
	url(r'^sign/', include(signx_urls)),
	url(r'^search/', include(search_urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns)