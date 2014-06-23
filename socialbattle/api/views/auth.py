from django.contrib.auth import login
from django.shortcuts import redirect
from social_auth.decorators import dsa_view
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from socialbattle.api.serializers import UserSerializer
from socialbattle.api.models import User

from social.apps.django_app.utils import strategy
from social.apps.django_app.default.models import UserSocialAuth

FACEBOOK_IMG_URL = 'https://graph.facebook.com/%s/picture?type=normal'

@strategy('social:complete')
@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def associate_by_access_token(request, backend, *args, **kwargs):
	access_token = request.GET.get('access_token')
	backend = request.strategy.backend
	user = backend.do_auth(access_token, user=request.user)
	if user and user.is_active:
		f_uid = UserSocialAuth.objects.values('uid').get(user_id=user.pk)['uid']
		user.img = FACEBOOK_IMG_URL % f_uid
		user.set_unusable_password() #in the way that the user cannot login without facebook
		user.save()
		data = UserSerializer(user, context={'request': request}).data
		return Response(data, status=status.HTTP_200_OK)
	return Response(status=status.HTTP_400_BAD_REQUEST)

from socialbattle.api import pusher
from pusher import Channel
@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def pusher_auth(request, *args, **kwargs):
	channel_name = request.DATA['channel_name']
	socket_id = request.DATA['socket_id']
	
	channel = Channel(channel_name, pusher)
	r = channel.authenticate(socket_id)
	return Response(r, status=status.HTTP_200_OK)

class SignupViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
	model = User
	serializer_class = UserSerializer
	permission_classes = [AllowAny, ]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if serializer.is_valid():
			user = serializer.object
			username = user.username
			email = user.email
			password = user.password
			user = User.objects.create_user(username, email, password)
			user = self.get_serializer(user).data
			return Response(user, status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
