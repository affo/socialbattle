from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.decorators import api_view, renderer_classes, permission_classes, action
from rest_framework.reverse import reverse
from socialbattle.api import models
from socialbattle.api import serializers

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