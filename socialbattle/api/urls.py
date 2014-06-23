from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from socialbattle.api.views import user, ability, character, item, mob, \
		post, room, transaction, auth, action, gift, notification
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
router.register(r'signup', auth.SignupViewSet)

router.register(r'gifts', gift.GiftViewSet)
router.register(r'notifications', notification.NotificationViewSet)
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/notifications',
		notification.UserNotificationViewSet,
		base_name='usernotification'
)
router.register(r'users/(?P<username>[a-zA-Z0-9-_]+)/notifications/unread',
		notification.UserUnreadNotificationViewSet,
		base_name='userunreadnotification'
)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.status import HTTP_200_OK
# @api_view(['GET'])
# def push(request):
# 	from socialbattle.api import pusher
# 	msg = request.QUERY_PARAMS.get('msg', None)

# 	if msg is None:
# 		msg = "empty msg"

# 	data = {'message': msg}

# 	pusher['test_channel'].trigger('api_event', data)

# 	return Response(data, status=HTTP_200_OK)



urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^me/$', user.me),
	url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	url(r'^sa/default/', include('social.apps.django_app.urls', namespace='social')),
	url(r'^sa/associate/(?P<backend>[a-z]+)/', auth.associate_by_access_token),
	url(r'^pusher/auth/$', auth.pusher_auth),

	url(r'^rpg/dmg/$', action.damage),
	url(r'^rpg/exp/$', action.exp),
	url(r'^rpg/ct/$', action.ct),
	url(r'^rpg/stat/$', action.stat),
)

#use in the future for a personal template!
# urlpatterns += patterns('',
# 	#required by DOT
# 	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'api/login.html'}),
# )