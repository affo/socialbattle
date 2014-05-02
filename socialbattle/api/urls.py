from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import access, social, battle

signx_urls = patterns('',
	url(r'^up/$', access.signup, name='signup'),
	url(r'^in/$', 'rest_framework.authtoken.views.obtain_auth_token', name='signin'),
	url(r'^out/$', access.signout, name='signout'),
)

follow_detail_view = social.FollowDetailViewSet.as_view({
	'delete': 'destroy',
})

user_post_list_view = social.UserPostListViewSet.as_view({
	'get': 'list',
})

post_detail_view = social.PostDetailViewSet.as_view({
	'get': 'retrieve',
	'delete': 'destroy',
	'put': 'update',
})
comment_detail_view = social.CommentDetailViewSet.as_view({
	'get': 'retrieve',
	'delete': 'destroy',
	'put': 'update',
})

follow_urls = patterns('',
	url(r'^(?P<pk>\d+)/$', follow_detail_view, name='fellowship-detail'),
	url(r'^$', social.FollowListViewSet.as_view({'post': 'create'}), name='fellowship-create')
)

user_follow_urls = patterns('',
	url(r'^follow(?P<direction>[(ers)|(ing)]+)/$', social.FollowListViewSet.as_view({'get': 'followx'}), name='fellowship-list'),
)

user_post_urls = patterns('',
	url(r'^posts/$', user_post_list_view, name='user_post-list'),
)

room_post_urls = patterns('',
	url(r'^posts/$', social.RelaxRoomPostListViewSet.as_view({'get': 'list', 'post': 'create'}), name='room_post-list'),
)

post_urls = patterns('',
	url(r'^(?P<pk>\d+)/$', post_detail_view, name='post-detail'),
	url(r'^(?P<pk>\d+)/comments/$', social.PostCommentListViewSet.as_view({'get': 'list', 'post': 'create'}), name='post_comment-list'),
)

comment_urls = patterns('',
	url(r'^(?P<pk>\d+)/$', comment_detail_view, name='comment-detail'),
)

user_urls = patterns('',
	url(r'^(?P<username>[0-9a-zA-Z_-]+)/characters/$', battle.UserCharacterList.as_view(), name='usercharacter-list'),
	url(r'^(?P<username>[0-9a-zA-Z_-]+)/$', social.UserDetail.as_view(), name='user-detail'),
	url(r'^$', social.UserList.as_view(), name='user-list'),

	url(r'^(?P<username>[0-9a-zA-Z_-]+)/', include(user_follow_urls)),
	url(r'^(?P<username>[0-9a-zA-Z_-]+)/', include(user_post_urls)),
)

search_urls = patterns('',
	url(r'^users/$', access.search_user, name='user-search'),
	url(r'^characters/$', access.search_character, name='character-search'),
	url(r'^rooms/$', access.search_room, name='room-search'),
)

character_urls = patterns('',
	url(r'^(?P<name>[0-9a-zA-Z_-]+)/$', battle.CharacterDetail.as_view(), name='character-detail'),
	url(r'^$', battle.CharacterList.as_view(), name='character-list'),
)

room_urls = patterns('',
	#url(r'^relax/$', RelaxRoomList.as_view(), name='relaxroom-list'),
	url(r'^pve/$', battle.PVERoomList.as_view(), name='pveroom-list'),
	url(r'^relax/(?P<name>[0-9a-zA-Z_-]+)/$', battle.RelaxRoomDetail.as_view(), name='relaxroom-detail'),
	url(r'^pve/(?P<name>[0-9a-zA-Z_-]+)/$', battle.PVERoomDetail.as_view(), name='pveroom-detail'),
	url(r'^$', battle.RoomList.as_view(), name='room-list'),

	url(r'^relax/(?P<name>[0-9a-zA-Z_-]+)/', include(room_post_urls)),
)

mob_urls = patterns('',
	url(r'^(?P<name>[0-9a-zA-Z_-]+)/$', battle.MobDetail.as_view(), name='mob-detail'),
)

item_urls = patterns('',
	url(r'^(?P<pk>[0-9a-zA-Z_-]+)/$', battle.ItemDetail.as_view(), name='item-detail'),
)

urlpatterns = patterns('',
	url(r'^$', access.api_root, name='api-root'),
	url(r'^users/', include(user_urls)),
	url(r'^characters/', include(character_urls)),
	url(r'^rooms/', include(room_urls)),
	url(r'^mobs/', include(mob_urls)),
	url(r'^items/', include(item_urls)),
	url(r'^sign/', include(signx_urls)),
	url(r'^search/', include(search_urls)),
	url(r'^fellowships/', include(follow_urls)),
	url(r'^posts/', include(post_urls)),
	url(r'^comments/', include(comment_urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns)