from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import access, social, battle

# signx_urls = patterns('',
# 	url(r'^up/$', access.signup, name='signup'),
# 	url(r'^in/$', 'rest_framework.authtoken.views.obtain_auth_token', name='signin'),
# 	url(r'^out/$', access.signout, name='signout'),
# )

# delete = {'delete': 'destroy'}
# post = {'post': 'create'}
# detail = {
# 			'get': 'retrieve',
# 			'delete': 'destroy',
# 			'put': 'update',
# 		}
# get_list = {'get': 'list'}
# get_post_list = {'get': 'list', 'post': 'create'}
# get_delete = {'get': 'retrieve', 'delete': 'destroy'}

# follow_urls = patterns('',
# 	url(r'^(?P<pk>\d+)/$', social.FollowViewSet.as_view(get_delete), name='fellowship-detail'),
# 	url(r'^$', social.FollowViewSet.as_view(post), name='fellowship-create')
# )

# user_follow_urls = patterns('',
# 	url(r'^following/$', social.FollowViewSet.as_view({'get': 'following'}), name='fellowship-list'),
# 	url(r'^followers/$', social.FollowViewSet.as_view({'get': 'followers'}), name='fellowship-list'),
# )

# user_post_urls = patterns('',
# 	url(r'^posts/$', social.PostViewset.as_view(get_list), name='userpost-list'),
# )

# room_post_urls = patterns('',
# 	url(r'^posts/$', social.PostViewset.as_view(get_post_list), name='roompost-list'),
# )
# room_mob_urls = patterns('',
# 	url(r'^mobs/$', battle.MobViewSet.as_view(get_list), name='roommob-list'),
# )

# post_urls = patterns('',
# 	url(r'^(?P<pk>\d+)/$', social.PostViewset.as_view(detail), name='post-detail'),
# 	url(r'^(?P<post_pk>\d+)/comments/$', social.CommentViewSet.as_view(get_post_list), name='postcomment-list'),
# )

# comment_urls = patterns('',
# 	url(r'^(?P<pk>\d+)/$', social.CommentViewSet.as_view(detail), name='comment-detail'),
# )

# user_urls = patterns('',
# 	url(r'^(?P<username>[0-9a-zA-Z_-]+)/characters/$', battle.CharacterViewSet.as_view(get_post_list), name='usercharacter-list'),
# 	url(r'^(?P<username>[0-9a-zA-Z_-]+)/$', social.UserViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='user-detail'),
# 	url(r'^$', social.UserViewSet.as_view({'get': 'list'}), name='user-list'),

# 	url(r'^(?P<username>[0-9a-zA-Z_-]+)/', include(user_follow_urls)),
# 	url(r'^(?P<username>[0-9a-zA-Z_-]+)/', include(user_post_urls)),
# )

# search_urls = patterns('',
# 	url(r'^users/$', access.search_user, name='user-search'),
# 	url(r'^characters/$', access.search_character, name='character-search'),
# 	url(r'^rooms/$', access.search_room, name='room-search'),
# )

# character_nested_urls = patterns('',
# 	url(r'^abilities/$', battle.CharacterAbilityList.as_view(get_list), name='character_ability-list'),
# 	url(r'^inventory/$', battle.CharacterInventory.as_view(get_post_list), name='character_item-list'),
# 	url(r'^inventory/(?P<pk>\d+)/$', battle.CharacterInventory.as_view(delete), name='character_item-delete'),
# 	url(r'^next_abilities/$', battle.CharacterAbilityList.as_view({'get': 'next'}), name='nextability-list'),
# )

# character_urls = patterns('',
# 	url(r'^(?P<name>[0-9a-zA-Z_-]+)/$', battle.CharacterViewSet.as_view(get_delete), name='character-detail'),
# 	url(r'^(?P<name>[0-9a-zA-Z_-]+)/', include(character_nested_urls)),
# )

# room_urls = patterns('',
# 	#url(r'^relax/$', RelaxRoomList.as_view(), name='relaxroom-list'),
# 	url(r'^pve/$', battle.PVERoomList.as_view(), name='pveroom-list'),
# 	url(r'^relax/(?P<name>[0-9a-zA-Z_-]+)/$', battle.RelaxRoomDetail.as_view({'get': 'retrieve'}), name='relaxroom-detail'),
# 	url(r'^pve/(?P<name>[0-9a-zA-Z_-]+)/$', battle.PVERoomDetail.as_view({'get': 'retrieve'}), name='pveroom-detail'),
# 	url(r'^$', battle.RoomList.as_view(), name='room-list'),

# 	url(r'^relax/(?P<name>[0-9a-zA-Z_-]+)/', include(room_post_urls)),
# 	url(r'^pve/(?P<room_name>[0-9a-zA-Z_-]+)/', include(room_mob_urls)),
# )

# mob_urls = patterns('',
# 	url(r'^(?P<name>[0-9a-zA-Z_-]+)/$', battle.MobViewSet.as_view({'get': 'retrieve'}), name='mob-detail'),
# )

# item_nested_urls = patterns('',
# 	url(r'^buy/$', battle.ItemDetail.as_view({'get': 'buy'}), name='item-buy'),
# 	url(r'^sell/$', battle.ItemDetail.as_view({'get': 'sell'}), name='item-sell'),
# 	url(r'^equip/$', battle.ItemDetail.as_view({'get': 'equip'}), name='item-equip'),
# )

# item_urls = patterns('',
# 	url(r'^(?P<pk>\d+)/$', battle.ItemDetail.as_view({'get': 'retrieve'}), name='item-detail'),
# 	url(r'^(?P<pk>\d+)/', include(item_nested_urls)),
# )

# inventory_urls = patterns('',
# 	url(r'^(?P<pk>\d+)/$', battle.InventoryRecordDetail.as_view(get_delete), name='inventoryrecord-detail'),
# )

# ability_urls = patterns('',
# 	url(r'^phys/(?P<pk>\d+)/$', battle.PhysicalAbilityDetail.as_view({'get': 'retrieve'}), name='physicalability-detail'),
# 	url(r'^white/(?P<pk>\d+)/$', battle.WhiteMagicAbilityDetail.as_view({'get': 'retrieve'}), name='whitemagicability-detail'),
# 	url(r'^black/(?P<pk>\d+)/$', battle.BlackMagicAbilityDetail.as_view({'get': 'retrieve'}), name='blackmagicability-detail'),
# )

# urlpatterns = patterns('',
# 	url(r'^$', access.api_root, name='api-root'),
# 	url(r'^users/', include(user_urls)),
# 	url(r'^characters/', include(character_urls)),
# 	url(r'^rooms/', include(room_urls)),
# 	url(r'^mobs/', include(mob_urls)),
# 	url(r'^items/', include(item_urls)),
# 	url(r'^sign/', include(signx_urls)),
# 	url(r'^search/', include(search_urls)),
# 	url(r'^fellowships/', include(follow_urls)),
# 	url(r'^posts/', include(post_urls)),
# 	url(r'^comments/', include(comment_urls)),
# 	url(r'^abilities/', include(ability_urls)),
# 	url(r'^inventory/', include(inventory_urls)),
# )
#############
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register(r'users', social.UserViewSet, base_name='user')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/following', social.UserFollowingViewSet, base_name='userfollow')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/followers', social.UserFollowersViewSet, base_name='userfollow')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/posts', social.UserPostViewSet, base_name='userpost')
router.register(r'fellowship', social.FellowshipViewSet, base_name='fellowship')

router.register(r'rooms', battle.RoomViewSet, base_name='room')
router.register(r'rooms/relax', battle.RelaxRoomViewSet, base_name='relaxroom')
router.register(r'rooms/relax/(?P<room_name>[a-zA-Z0-9-_]+)/posts', social.RoomPostViewSet, base_name='roompost')
router.register(r'rooms/relax/(?P<room_name>[a-zA-Z0-9-_]+)/items', battle.RoomItemViewSet, base_name='roomitem')
router.register(r'rooms/pve', battle.PVERoomViewSet, base_name='pveroom')
router.register(r'rooms/pve/(?P<room_name>[a-zA-Z0-9-_]+)/mobs', battle.RoomMobViewSet, base_name='roommob')
router.register(r'posts', social.PostViewset, base_name='post')
router.register(r'posts/(?P<pk>\d+)/comments', social.PostCommentViewSet, base_name='postcomment')
router.register(r'comments', social.CommentViewSet, base_name='comment')

router.register(r'items', battle.ItemViewSet, base_name='item')
router.register(r'mobs', battle.MobViewSet, base_name='mob')
urlpatterns = patterns('', url(r'^', include(router.urls)))