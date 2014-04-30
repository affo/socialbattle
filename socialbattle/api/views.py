from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, renderer_classes, permission_classes, action
from rest_framework.reverse import reverse
from rest_framework import viewsets
import models
import serializers

#from announce import AnnounceClient
#announce_client = AnnounceClient()

@api_view(['GET'])
@permission_classes([permissions.AllowAny, ])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'rooms': reverse('room-list', request=request, format=format),
		'characters': reverse('character-list', request=request, format=format),
		})


#remember:
# Custom actions which use the @link decorator will respond to GET requests.
# We could have instead used the @action decorator if we wanted an action that responded to POST requests.
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

@api_view(['POST', ])
@renderer_classes((JSONRenderer, ))
def signup(request, format=None):
		username = request.DATA['username']
		password = request.DATA['password']
		email = request.DATA['email']

		user = models.User.objects.create_user(username, email, password)
		user = serializers.UserSerializer(user).data
		return Response(user)

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
@api_view(['POST', ])
@renderer_classes((JSONRenderer, ))
@permission_classes([permissions.IsAuthenticated, ])
def signout(request, format=None):
	logout(request)
	return Response(
			data={'message': 'Logged out successfully'},
			status=status.HTTP_200_OK
			)

@api_view(['GET', ])
@renderer_classes((JSONRenderer, ))
@permission_classes([permissions.IsAuthenticated, ])
def search_user(request, format=None):
		query = request.DATA['query']

		from django.db.models import Q
		users = models.User.objects.filter(
				Q(username__icontains=query) |
				Q(first_name__icontains=query) |
				Q(last_name__icontains=query)
			)

		return Response(serializers.UserSerializer(users).data)

@api_view(['GET', ])
@renderer_classes((JSONRenderer, ))
@permission_classes([permissions.IsAuthenticated, ])
def search_character(request, format=None):
		query = request.DATA['query']
		characters = models.Character.objects.filter(name__icontains=query)
		return Response(serializers.CharacterSerializer(characters).data)

#modify the model accordingly
@api_view(['GET', ])
@renderer_classes((JSONRenderer, ))
@permission_classes([permissions.IsAuthenticated, ])
def search_room(request, format=None):
		query = request.DATA['query']
		rooms = models.Room.objects.filter(name__icontains=query)
		return Response(serializers.RoomSerializer(rooms).data)


### SOCIAL PART ###
@api_view(['GET', ])
@renderer_classes((JSONRenderer, ))
#@permission_classes([permissions.IsAuthenticated, ])
def followx(request, username, direction, format=None):
	if direction == 'ing':
		follows = models.User.objects.get(username=username).follows.all()
		data = {'users': serializers.UserSerializer(follows).data}
	elif direction == 'ers':
		from django.db.models import F
		#followed = models.User.objects.filter(username=username, pk__in=F('follows'))
		#data = {'users': serializers.UserSerializer(followed).data}
	else:
		message = "A user is followING or has followERS, a user cannot be/have follow%s" % direction
		return Response(data={'message': message}, status=status.HTTP_400_BAD_REQUEST)

	return Response(data)

class FollowView(viewsets.GenericViewSet):
	queryset = models.Fellowship.objects.all()
	serializer_class = serializers.FellowshipSerializer
	permission_classes = [permissions.AllowAny, ]

	@action(methods=['GET', ])
	def followx(self, request, username, direction, format=None):
		if direction == 'ing':
			follows = self.get_queryset().filter(from_user__username=username).all().prefetch_related('to_user')
			follows = [f.to_user for f in follows]
			follows = serializers.UserSerializer(follows, context=self.get_serializer_context()).data
			data = {'users': follows}
		elif direction == 'ers':
			followed = self.get_queryset().filter(to_user__username=username).all().prefetch_related('from_user')
			followed = [f.from_user for f in followed]
			followed = serializers.UserSerializer(followed, context=self.get_serializer_context()).data
			data = {'users': followed}
		else:
			message = "A user is followING or has followERS, a user cannot be/have follow%s" % direction
			return Response(data={'message': message}, status=status.HTTP_400_BAD_REQUEST)
		return Response(data)

class UserList(generics.ListAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer
	#permission_classes = [permissions.IsAdminUser, ]

class UserDetail(generics.RetrieveUpdateAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer
	lookup_field = 'username'


class CharacterList(generics.ListCreateAPIView):
	model = models.Character
	serializer_class = serializers.CharacterSerializer
	permission_classes = [permissions.AllowAny]


class CharacterDetail(generics.RetrieveDestroyAPIView):
	model = models.Character
	serializer_class = serializers.CharacterSerializer
	permission_classes = [permissions.AllowAny]
	lookup_field = 'name'


class UserCharacterList(generics.ListAPIView):
	model = models.Character
	serializer_class = serializers.CharacterSerializer

	def get_queryset(self):
		queryset = super(UserCharacterList, self).get_queryset()
		return queryset.filter(owner__username=self.kwargs.get('username'))

class RelaxRoomDetail(generics.RetrieveAPIView):
	model = models.RelaxRoom
	serializer_class = serializers.RelaxRoomSerializer
	lookup_field = 'name'

class PVERoomList(generics.ListAPIView):
	model = models.PVERoom
	serializer_class = serializers.PVERoomSerializer

class PVERoomDetail(generics.RetrieveAPIView):
	model = models.PVERoom
	serializer_class = serializers.PVERoomSerializer
	lookup_field = 'name'

class RelaxRoomItemList(generics.ListAPIView):
	model = models.Item
	serializer_class = serializers.ItemSerializer

class PVERoomMobList(generics.ListAPIView):
	model = models.Mob
	serializer_class = serializers.MobSerializer

class MobDetail(generics.RetrieveAPIView):
	model = models.Mob
	serializer_class = serializers.MobSerializer
	lookup_field = 'name'

class ItemDetail(generics.RetrieveAPIView):
	model = models.Item
	serializer_class = serializers.ItemSerializer

from rest_framework.response import Response
class RoomList(generics.ListAPIView):

	def get(self, request, format=None):
		relax = models.RelaxRoom.objects.all()
		pve = models.PVERoom.objects.all()

		relax = serializers.RelaxRoomSerializer(relax, context=self.get_serializer_context()).data
		pve = serializers.PVERoomSerializer(pve, context=self.get_serializer_context()).data

		return Response(relax + pve)