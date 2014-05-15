from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import social, battle
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
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/inventory',
	battle.CharacterInventoryViewSet, base_name='characterinventory'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/transactions',
	battle.TransactionViewSet, base_name='charactertransaction'
)
router.register(
	r'characters/(?P<character_name>[a-zA-Z0-9-_]+)/battles',
	battle.CharacterBattleViewSet, base_name='characterbattle'
)

router.register(r'abilities', battle.AbilityViewSet)
router.register(r'inventory', battle.InventoryRecordViewSet)
router.register(r'battles', battle.BattleViewSet)
router.register(r'targets', battle.TargetViewSet)
urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^auth/', 'rest_framework.authtoken.views.obtain_auth_token')
)