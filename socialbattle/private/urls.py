from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from socialbattle.private.views import user, ability, character, item, mob, post, room, transaction
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register(r'users', user.UserViewSet)
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/following', user.UserFollowingViewSet, base_name='userfollow')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/followers', user.UserFollowersViewSet, base_name='userfollow')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/posts', post.UserPostViewSet, base_name='userpost')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/characters', character.UserCharacterViewSet, base_name='usercharacter')
router.register(r'fellowship', user.FellowshipViewSet)

router.register(r'rooms', room.RoomViewSet, base_name='room')
router.register(r'rooms/relax', room.RelaxRoomViewSet)
router.register(r'rooms/relax/(?P<room_slug>[a-zA-Z0-9-_]+)/posts', post.RoomPostViewSet, base_name='roompost')
router.register(r'rooms/relax/(?P<room_slug>[a-zA-Z0-9-_]+)/items', item.RoomItemViewSet, base_name='roomitem')
router.register(r'rooms/pve', room.PVERoomViewSet)
router.register(r'rooms/pve/(?P<room_slug>[a-zA-Z0-9-_]+)/mobs', mob.RoomMobViewSet, base_name='roommob')
router.register(r'posts', post.PostViewset)
router.register(r'posts/(?P<pk>\d+)/comments', post.PostCommentViewSet, base_name='postcomment')
router.register(r'comments', post.CommentViewSet)

router.register(r'items', item.ItemViewSet)
router.register(r'mobs', mob.MobViewSet)

router.register(r'characters', character.CharacterViewSet)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/abilities',
	ability.CharacterAbilityViewSet,
	base_name='characterability'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/abilities/next',
	ability.CharacterNextAbilityViewSet,
	base_name='characternextability'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/inventory',
	item.CharacterInventoryViewSet, base_name='characterinventory'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/transactions',
	transaction.TransactionViewSet, base_name='transaction'
)

router.register(r'inventory', item.InventoryRecordViewSet)
router.register(r'abilities', ability.AbilityViewSet)

urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
)