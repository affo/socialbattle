from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import access, social, battle
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register(r'users', social.UserViewSet)
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/following', social.UserFollowingViewSet, base_name='userfollow')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/followers', social.UserFollowersViewSet, base_name='userfollow')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/posts', social.UserPostViewSet, base_name='userpost')
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/characters', battle.UserCharacterViewSet, base_name='usercharacter')
router.register(r'fellowship', social.FellowshipViewSet)

router.register(r'rooms', battle.RoomViewSet, base_name='room')
router.register(r'rooms/relax', battle.RelaxRoomViewSet)
router.register(r'rooms/relax/(?P<room_slug>[a-zA-Z0-9-_]+)/posts', social.RoomPostViewSet, base_name='roompost')
router.register(r'rooms/relax/(?P<room_slug>[a-zA-Z0-9-_]+)/items', battle.RoomItemViewSet, base_name='roomitem')
router.register(r'rooms/pve', battle.PVERoomViewSet)
router.register(r'rooms/pve/(?P<room_slug>[a-zA-Z0-9-_]+)/mobs', battle.RoomMobViewSet, base_name='roommob')
router.register(r'posts', social.PostViewset)
router.register(r'posts/(?P<pk>\d+)/comments', social.PostCommentViewSet, base_name='postcomment')
router.register(r'comments', social.CommentViewSet)

router.register(r'items', battle.ItemViewSet)
router.register(r'mobs', battle.MobViewSet)

router.register(r'characters', battle.CharacterViewSet)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/abilities',
	battle.CharacterAbilityViewSet,
	base_name='characterability'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/abilities/next',
	battle.CharacterNextAbilityViewSet,
	base_name='characternextability'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/abilities/next/phys',
	battle.CharacterNextPhysicalAbilityViewSet,
	base_name='characternextphysicalability'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/abilities/next/black',
	battle.CharacterNextBlackAbilityViewSet,
	base_name='characternextblackability'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/abilities/next/white',
	battle.CharacterNextWhiteAbilityViewSet,
	base_name='characternextwhiteability'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/inventory',
	battle.CharacterInventoryViewSet, base_name='characterinventory')

router.register(r'abilities/phys', battle.PhysicalAbilityViewSet)
router.register(r'abilities/black', battle.BlackMagicAbilityViewSet)
router.register(r'abilities/white', battle.WhiteMagicAbilityViewSet)

router.register(r'inventory', battle.InventoryRecordViewSet)
urlpatterns = patterns('', url(r'^', include(router.urls)))