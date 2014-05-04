from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsOwner

class PVERoomMobList(viewsets.GenericViewSet, mixins.ListModelMixin):
	queryset = models.Mob.objects
	serializer_class = serializers.MobSerializer

	def get_queryset(self):
		room_name = self.kwargs.get('name')

		if room_name:
			return self.queryset.filter(pveroom__name=room_name).all()
		return None

class MobDetail(generics.RetrieveAPIView):
	model = models.Mob
	serializer_class = serializers.MobSerializer
	lookup_field = 'name'

class UserCharacterList(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
	queryset = models.Character.objects
	serializer_class = serializers.CharacterSerializer

	def get_queryset(self):
		return self.queryset.filter(owner__username=self.kwargs.get('username'))

	def pre_save(self, obj):
		obj.owner = self.request.user

	@action(methods=['GET'])
	def select(self, request, name, format=None):
		character = models.Character.objects.get(name=name)
		if character.owner != request.user:
			self.permission_denied(request)
		
		character = serializers.CharacterSerializer(character, context=self.get_serializer_context()).data
		request.session['character'] = character
		data = {
			'character': character,
			'msg': 'Character %s selected by user %s' % (character['name'], request.user.username, )
		}
		return Response(data)



class CharacterDetail(viewsets.GenericViewSet,
						mixins.DestroyModelMixin,
						mixins.RetrieveModelMixin,
						mixins.UpdateModelMixin):
	queryset = models.Character.objects.all()
	serializer_class = serializers.CharacterSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	lookup_field = 'name'

class CharacterAbilityList(viewsets.GenericViewSet, mixins.ListModelMixin):
	queryset = models.Ability.objects
	serializer_class = serializers.AbilitySerializer

	def get_queryset(self):
		return self.queryset.filter(character__name=self.kwargs.get('name'))

class CharacterItemList(viewsets.GenericViewSet, mixins.ListModelMixin):
	queryset = models.Item.objects
	serializer_class = serializers.ItemSerializer

	def get_queryset(self):
		return self.queryset.filter(character__name=self.kwargs.get('name'))

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

class ItemDetail(generics.RetrieveAPIView):
	model = models.Item
	serializer_class = serializers.ItemSerializer

class RoomList(generics.ListAPIView):

	def get(self, request, format=None):
		relax = models.RelaxRoom.objects.all()
		pve = models.PVERoom.objects.all()

		relax = serializers.RelaxRoomSerializer(relax, context=self.get_serializer_context()).data
		pve = serializers.PVERoomSerializer(pve, context=self.get_serializer_context()).data

		return Response(relax + pve)