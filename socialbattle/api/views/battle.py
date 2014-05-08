from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsOwner, IsOwnerCharacter

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
# GET, PUT, PATCH, DELETE: /characters/{character_name}/
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
# GET, POST: /characters/{character_name}/abilities/next/
# GET: /abilities/{ability_name}
class CharacterAbilityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the learned abilities for the chosen character
	'''
	def list(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		abilities = character.abilities.all()
		abilities = serializers.AbilitySerializer(abilities, context=self.get_serializer_context(), many=True).data
		return Response(data=abilities, status=status.HTTP_200_OK)

class CharacterNextAbilityViewSet(viewsets.GenericViewSet,
									mixins.ListModelMixin,
									mixins.CreateModelMixin):
	'''
		List of the available abilities that a character can learn
	'''
	serializer_class = serializers.LearntAbilitySerializer

	def list(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)

		next = character.get_next_abilities()
		next = serializers.AbilitySerializer(next, context=self.get_serializer_context(), many=True).data
		return Response(data=next, status=status.HTTP_200_OK)

	def create(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)

		if character.owner != request.user:
			self.permission_denied(request)

		serializer = serializers.LearntAbilitySerializer(data=request.DATA, files=request.FILES)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		to_learn = serializer.object
		ability = to_learn.ability
		if ability not in character.get_next_abilities():
			return Response({'msg': 'The ability specified cannot be learnt'},
							status=status.HTTP_400_BAD_REQUEST)

		if ability.ap_required > character.ap:
			return Response({'msg': 'Too much APs'},
							status=status.HTTP_400_BAD_REQUEST)

		character.ap -= ability.ap_required
		character.save()
		to_learn.character = character
		self.object = serializer.save(force_insert=True)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AbilityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.Ability.objects.all()
	serializer_class = serializers.AbilitySerializer
	lookup_field='slug'

### INVENTORY
# GET, DELETE, PUT: /inventory/{pk}/
# GET, POST: /characters/{character_name}/inventory/
class CharacterInventoryViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin, 
							mixins.CreateModelMixin):
	'''
		The inventory of the selected character.  
		From this view it is possible for a character to buy (`POST`) items.
	'''
	serializer_class = serializers.InventoryRecordCreateSerializer

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
		record = self.get_serializer(record).data
		data = {
			'msg': 'Item added to inventory',
			'inventory_record': record,
			'guils left': character.guils,
		}

		return Response(data=data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(data))

class InventoryRecordViewSet(viewsets.GenericViewSet,
							mixins.RetrieveModelMixin,
							mixins.DestroyModelMixin,
							mixins.UpdateModelMixin):
	'''
		Detailed view of an inventory record:
		It is possible to sell (`DELETE`) items.  
		It is possible to equip (`PUT`) items.
	'''
	queryset = models.InventoryRecord.objects.all()
	serializer_class = serializers.InventoryRecordUpdateSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerCharacter]

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
				if record.equipped == True:
					if item == character.current_weapon:
						character.current_weapon = None
					else:
						character.current_armor = None
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