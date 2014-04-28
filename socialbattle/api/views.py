from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, renderer_classes
import models
import serializers

#from announce import AnnounceClient
#announce_client = AnnounceClient()

# @api_view(['GET'])
# @renderer_classes((TemplateHTMLRenderer,))
# def root(request, format=None):
# 	return Response(template_name='base.html')

# @api_view(['GET'])
# def api_root(request, format=None):
# 	return Response({
# 		'players': reverse('player-list', request=request, format=format),
# 		'pve-rooms': reverse('pveroom-list', request=request, format=format),
# 		'relax-rooms': reverse('relaxroom-list', request=request, format=format),
# 		})


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
def signout(request, format=None):
	logout(request)
	return Response(
			data={'message': 'Logged out successfully'},
			status=status.HTTP_200_OK
			)

class UserList(generics.ListAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer
	permission_classes = [permissions.IsAuthenticated]


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


class UserCharacterList(generics.ListAPIView):
	model = models.Character
	serializer_class = serializers.CharacterSerializer

	def get_queryset(self):
		queryset = super(UserCharacterList, self).get_queryset()
		return queryset.filter(owner__username=self.kwargs.get('username'))

class RelaxRoomList(generics.ListAPIView):
	model = models.RelaxRoom
	serializer_class = serializers.RelaxRoomSerializer

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