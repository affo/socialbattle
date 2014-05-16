from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from socialbattle.private import models
from socialbattle.private import serializers
from socialbattle.private.permissions import IsOwner

### CHARACTER
# GET, POST: /users/{username}/characters/
# GET, DELETE: /characters/{character_name}/
class UserCharacterViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin,
							mixins.CreateModelMixin):
	'''
		List of characters for the chosen user
	'''
	serializer_class = serializers.CharacterSerializer

	def get_queryset(self):
		queryset = models.Character.objects.all()
		username = self.kwargs.get('username')
		if username:
			queryset = queryset.filter(owner__username=username).all()
		return queryset

	def pre_save(self, obj):
		obj.owner = self.request.user

	def post_save(self, obj, created=False):
		if created:
			obj.physical_abilities.add(models.PhysicalAbility.objects.get(name='attack'))
			obj.white_magic_abilities.add(models.WhiteMagicAbility.objects.get(name='cure'))
			obj.black_magic_abilities.add(models.BlackMagicAbility.objects.get(name='fire'))
			obj.black_magic_abilities.add(models.BlackMagicAbility.objects.get(name='thunder'))
			potion = models.Item.objects.get(name='potion')
			record = models.InventoryRecord.objects.create(owner=obj, item=potion, quantity=3)

from socialbattle.private.views.action import ActionMixin
class CharacterViewSet(viewsets.GenericViewSet,
						mixins.RetrieveModelMixin,
						mixins.DestroyModelMixin,
						mixins.ListModelMixin,
						ActionMixin):
	queryset = models.Character.objects.all()
	serializer_class = serializers.CharacterSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	lookup_field = 'name'

	def list(self, request, *args, **kwargs):
		try:
			query = request.QUERY_PARAMS['query']
		except:
			return Response(data={'msg': 'Query param needed (?query=<query_string>)'},
							status=status.HTTP_400_BAD_REQUEST)

		characters = models.Character.objects.filter(name__icontains=query)
		return Response(serializers.CharacterSerializer(characters, context=self.get_serializer_context(), many=True).data,
						status=status.HTTP_200_OK)

	@action(methods=['GET', ], serializer_class=serializers.ItemSerializer)
	def weapon(self, request, *args, **kwargs):
		character = self.get_object()
		weapon = character.get_weapon()
		serializer = self.get_serializer(weapon)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@action(methods=['GET', ], serializer_class=serializers.ItemSerializer)
	def armor(self, request, *args, **kwargs):
		character = self.get_object()
		armor = character.get_armor()
		serializer = self.get_serializer(armor)
		return Response(serializer.data, status=status.HTTP_200_OK)