from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import get_object_or_404
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsOwner

### ROOM
# GET: /rooms/
# GET: /rooms/pve/
# GET: /rooms/pve/{room_slug}
# GET: /rooms/relax/
# GET: /rooms/relax/{room_slug}
class RelaxRoomViewSet(viewsets.GenericViewSet,
						mixins.ListModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.RelaxRoom.objects.all()
	serializer_class = serializers.RelaxRoomSerializer
	lookup_field = 'slug'

class PVERoomViewSet(viewsets.GenericViewSet,
						mixins.ListModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.PVERoom.objects.all()
	serializer_class = serializers.PVERoomSerializer
	lookup_field = 'slug'

class RoomViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of all rooms (pve and relax)
	'''

	def list(self, request, *args, **kwargs):
		try:
			query = request.QUERY_PARAMS['query']
			relax = models.RelaxRoom.objects.filter(name__icontains=query)
			pve = models.PVERoom.objects.filter(name__icontains=query)
		except:
			relax = models.RelaxRoom.objects.all()
			pve = models.PVERoom.objects.all()

		relax = serializers.RelaxRoomSerializer(relax, context=self.get_serializer_context(), many=True).data
		pve = serializers.PVERoomSerializer(pve, context=self.get_serializer_context(), many=True).data

		return Response(relax + pve, status=status.HTTP_200_OK)

### MOB
# GET: /room/pve/{room_slug}/mobs/
# GET: /mobs/{mob_name}
class RoomMobViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available mobs for the chosen PVE room
	'''
	serializer_class = serializers.MobSerializer

	def get_queryset(self):
		queryset = models.Mob.objects.all()
		room_slug = self.kwargs.get('room_slug')
		if room_slug:
			queryset = queryset.filter(pveroom__slug=room_slug).all()
		return queryset

class MobViewSet(viewsets.GenericViewSet, generics.RetrieveAPIView):
	'''
		List of the available mobs for the chosen PVE room
	'''
	queryset = models.Mob.objects.all()
	serializer_class = serializers.MobSerializer
	lookup_field = 'slug'

### ITEM
# GET: /room/relax/{room_slug}/items/
# GET: /items/{item_name}/
class ItemViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	model = models.Item
	serializer_class = serializers.ItemSerializer
	lookup_field = 'slug'

class RoomItemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available items for the chosen relax room
	'''
	serializer_class = serializers.ItemSerializer

	def get_queryset(self):
		queryset = models.Item.objects.all()
		room_slug = self.kwargs.get('room_slug')
		if room_slug:
			queryset = queryset.filter(relaxroom__slug=room_slug).all()
		return queryset

### CHARACTER
# GET, POST: /users/{username}/characters/
# GET, PUT, DELETE: /characters/{character_name}/
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

class CharacterViewSet(viewsets.GenericViewSet,
						mixins.RetrieveModelMixin,
						mixins.DestroyModelMixin,
						mixins.UpdateModelMixin,
						mixins.ListModelMixin):
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

### ABILITY
# GET: /characters/{character_name}/abilities/	
# GET: /characters/{character_name}/abilities/next/
# GET, POST: /characters/{character_name}/abilities/next/phys/
# GET, POST: /characters/{character_name}/abilities/next/black/
# GET, POST: /characters/{character_name}/abilities/next/white/
# GET: /abilities/phys/{ability_name}
# GET: /abilities/black/{ability_name}
# GET: /abilities/white/{ability_name}
class CharacterAbilityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the learned abilities for the chosen character
	'''
	def list(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		physical = character.physical_abilities.all()
		white = character.white_magic_abilities.all()
		black = character.black_magic_abilities.all()

		physical = serializers.PhysicalAbilitySerializer(physical, context=self.get_serializer_context(), many=True).data
		white = serializers.WhiteMagicAbilitySerializer(white, context=self.get_serializer_context(), many=True).data
		black = serializers.BlackMagicAbilitySerializer(black, context=self.get_serializer_context(), many=True).data
		return Response(data={
					'physical': physical,
					'white_magic': white,
					'black_magic': black,
				}, status=status.HTTP_200_OK)

class CharacterNextAbilityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available abilities that a character can learn
	'''
	def list(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)

		next_physical = character.get_next_physical_abilities()
		next_black = character.get_next_black_abilities()
		next_white = character.get_next_white_abilities()

		next_physical = serializers.PhysicalAbilitySerializer(next_physical, context=self.get_serializer_context(), many=True).data
		next_white = serializers.WhiteMagicAbilitySerializer(next_white, context=self.get_serializer_context(), many=True).data
		next_black = serializers.BlackMagicAbilitySerializer(next_black, context=self.get_serializer_context(), many=True).data
		return Response(data={
					'physical': next_physical,
					'white_magic': next_white,
					'black_magic': next_black,
				})

class CharacterNextPhysicalAbilityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = serializers.PhysicalAbilitySerializer
	lookup_field = 'slug'

	def get_queryset(self):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		return character.get_next_physical_abilities()

class CharacterNextWhiteAbilityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = serializers.WhiteMagicAbilitySerializer
	lookup_field = 'slug'

	def get_queryset(self):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		return character.get_next_white_abilities()

class CharacterNextBlackAbilityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = serializers.BlackMagicAbilitySerializer
	lookup_field = 'slug'

	def get_queryset(self):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		return character.get_next_black_abilities()

class PhysicalAbilityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.PhysicalAbility.objects.all()
	serializer_class = serializers.PhysicalAbilitySerializer
	lookup_field='slug'

class WhiteMagicAbilityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.WhiteMagicAbility.objects.all()
	serializer_class = serializers.WhiteMagicAbilitySerializer
	lookup_field='slug'

class BlackMagicAbilityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.BlackMagicAbility.objects.all()
	serializer_class = serializers.BlackMagicAbilitySerializer
	lookup_field='slug'

### INVENTORY
# GET, DELETE: /inventory/{pk}/
# GET, POST: /characters/{character_name}/inventory/
class CharacterInventoryViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin, 
							mixins.CreateModelMixin):
	'''
		The inventory of the selected character.  
		From this view it is possible for a character to buy (`POST`) items.
	'''
	serializer_class = serializers.InventoryRecordSerializer

	def get_queryset(self):
		queryset = models.InventoryRecord.objects.all()
		name = self.kwargs.get('character_name')
		if name:
			queryset = queryset.filter(owner__name=name)
		return queryset

	def create(self, request, *args, **kwargs):
		'''
			Buy action
		'''
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)

		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		req_record = serializer.object
		req_record.owner = character
		if req_record.owner.owner != request.user:
			self.permission_denied(request)

		if req_record.item.cost * req_record.quantity > character.guils:
			return Response(
						data={'msg': 'Not enough money to buy this item'},
					)

		try:
			record = models.InventoryRecord.objects.get(owner=req_record.owner, item=req_record.item)
			record.quantity += req_record.quantity
			record.save()
		except ObjectDoesNotExist:
			record = models.InventoryRecord.objects.create(owner=req_record.owner, item=req_record.item)

		character.guils -= (req_record.item.cost * req_record.quantity)
		character.save()
		record = serializers.InventoryRecordSerializer(record, context=self.get_serializer_context()).data
		data = {
			'msg': 'Item added to inventory',
			'inventory_record': record,
			'guils left': character.guils,
		}

		return Response(data=data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(data))

class InventoryRecordViewSet(viewsets.GenericViewSet,
							mixins.RetrieveModelMixin,
							mixins.DestroyModelMixin):
	'''
		Detailed view of an inventory record:
		It is possible to sell (`DELETE`) items.
	'''
	queryset = models.InventoryRecord.objects.all()
	serializer_class = serializers.InventoryRecordSerializer

	def destroy(self, request, *args, **kwargs):
		'''
			Sell action
		'''
		record = self.get_object()
		character = record.owner
		item = record.item
		if character.owner != request.user:
			self.permission_denied(request)

		try:
			record.quantity -= 1
			if record.quantity == 0:
				record.delete()
			else:
				record.save()
		except ObjectDoesNotExist:
			return Response(
					data={'msg': 'The specified character does not own the specified item'},
					status=status.HTTP_400_BAD_REQUEST
				)

		character.guils += item.cost #maybe item.cost/2
		character.save()
		record = serializers.InventoryRecordSerializer(record, context=self.get_serializer_context()).data
		data = {
			'msg': 'Item %s sold' % item.name,
			'inventory_record': record,
			'guils left': character.guils,
		}

		return Response(data=data)