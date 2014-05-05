from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import access, social, battle

signx_urls = patterns('',
	url(r'^up/$', access.signup, name='signup'),
	url(r'^in/$', 'rest_framework.authtoken.views.obtain_auth_token', name='signin'),
	url(r'^out/$', access.signout, name='signout'),
)

delete = {'delete': 'destroy'}
post = {'post': 'create'}
detail = {
			'get': 'retrieve',
			'delete': 'destroy',
			'put': 'update',
		}
get_list = {'get': 'list'}
get_post_list = {'get': 'list', 'post': 'create'}
put_delete = {'get': 'retrieve', 'delete': 'destroy'}

follow_urls = patterns('',
	url(r'^(?P<pk>\d+)/$', social.FollowDetail.as_view(delete), name='fellowship-detail'),
	url(r'^$', social.FollowList.as_view(post), name='fellowship-create')
)

user_follow_urls = patterns('',
	url(r'^follow(?P<direction>[(ers)|(ing)]+)/$', social.FollowList.as_view({'get': 'followx'}), name='fellowship-list'),
)

user_post_urls = patterns('',
	url(r'^posts/$', social.UserPostList.as_view(get_list), name='user_post-list'),
)

room_post_urls = patterns('',
	url(r'^posts/$', social.RelaxRoomPostList.as_view(get_post_list), name='room_post-list'),
)
room_mob_urls = patterns('',
	url(r'^mobs/$', battle.PVERoomMobList.as_view(get_list), name='room_mob-list'),
)

post_urls = patterns('',
	url(r'^(?P<pk>\d+)/$', social.PostDetail.as_view(detail), name='post-detail'),
	url(r'^(?P<pk>\d+)/comments/$', social.PostCommentList.as_view(get_post_list), name='post_comment-list'),
)

comment_urls = patterns('',
	url(r'^(?P<pk>\d+)/$', social.CommentDetail.as_view(detail), name='comment-detail'),
)

user_urls = patterns('',
	url(r'^(?P<username>[0-9a-zA-Z_-]+)/characters/$', battle.UserCharacterList.as_view(get_post_list), name='user_character-list'),
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

character_nested_urls = patterns('',
	url(r'^abilities/$', battle.CharacterAbilityList.as_view(get_list), name='character_ability-list'),
	url(r'^items/$', battle.CharacterItemList.as_view(get_list), name='character_item-list'),
	url(r'^select/$', battle.CharacterDetail.as_view({'get': 'select'}), name='character-select'),
)

character_urls = patterns('',
	url(r'^(?P<name>[0-9a-zA-Z_-]+)/$', battle.CharacterDetail.as_view(detail), name='character-detail'),
	url(r'^(?P<name>[0-9a-zA-Z_-]+)/', include(character_nested_urls)),
)

room_urls = patterns('',
	#url(r'^relax/$', RelaxRoomList.as_view(), name='relaxroom-list'),
	url(r'^pve/$', battle.PVERoomList.as_view(), name='pveroom-list'),
	url(r'^relax/(?P<name>[0-9a-zA-Z_-]+)/$', battle.RelaxRoomDetail.as_view({'get': 'retrieve'}), name='relaxroom-detail'),
	url(r'^pve/(?P<name>[0-9a-zA-Z_-]+)/$', battle.PVERoomDetail.as_view({'get': 'retrieve'}), name='pveroom-detail'),
	url(r'^$', battle.RoomList.as_view(), name='room-list'),

	url(r'^relax/(?P<name>[0-9a-zA-Z_-]+)/', include(room_post_urls)),
	url(r'^relax/(?P<name>[0-9a-zA-Z_-]+)/enter/$', battle.RelaxRoomDetail.as_view({'get': 'enter'}), name='realxroom-select'),
	url(r'^pve/(?P<name>[0-9a-zA-Z_-]+)/', include(room_mob_urls)),
	url(r'^pve/(?P<name>[0-9a-zA-Z_-]+)/enter/$', battle.PVERoomDetail.as_view({'get': 'enter'}), name='pveroom-select'),
)

mob_urls = patterns('',
	url(r'^(?P<name>[0-9a-zA-Z_-]+)/$', battle.MobDetail.as_view(), name='mob-detail'),
)

item_urls = patterns('',
	url(r'^(?P<pk>[0-9a-zA-Z_-]+)/$', battle.ItemDetail.as_view(), name='item-detail'),
)

inventory_urls = patterns('',
	url(r'^(?P<pk>\d+)/$', battle.InventoryRecordDetail.as_view(put_delete), name='inventoryrecord-detail'),
)

ability_urls = patterns('',
	url(r'^phys/(?P<pk>\d+)/$', battle.PhysicalAbilityDetail.as_view({'get': 'retrieve'}), name='physicalability-detail'),
	url(r'^white/(?P<pk>\d+)/$', battle.WhiteMagicAbilityDetail.as_view({'get': 'retrieve'}), name='whitemagicability-detail'),
	url(r'^black/(?P<pk>\d+)/$', battle.BlackMagicAbilityDetail.as_view({'get': 'retrieve'}), name='blackmagicability-detail'),
)

current_urls = patterns('',
	url(r'^next_abilities/$', battle.CharacterNextAbilityList.as_view(get_list), name='nextability-list'),
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
	url(r'^abilities/', include(ability_urls)),
	url(r'^current/', include(current_urls)),
	url(r'^inventory/', include(inventory_urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns)