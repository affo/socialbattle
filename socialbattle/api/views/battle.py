from django.core.exceptions import ObjectDoesNotExist
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
# GET: /rooms/pve/{room_name}
# GET: /rooms/relax/
# GET: /rooms/relax/{room_name}
class RelaxRoomViewSet(viewsets.GenericViewSet,
						mixins.ListModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.RelaxRoom.objects.all()
	serializer_class = serializers.RelaxRoomSerializer
	lookup_field = 'name'

class PVERoomViewSet(viewsets.GenericViewSet,
						mixins.ListModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.PVERoom.objects.all()
	serializer_class = serializers.PVERoomSerializer
	lookup_field = 'name'

class RoomViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of all rooms (pve and relax)
	'''
	def list(self, request, *args, **kwargs):
		relax = models.RelaxRoom.objects.all()
		pve = models.PVERoom.objects.all()

		relax = serializers.RelaxRoomSerializer(relax, context=self.get_serializer_context(), many=True).data
		pve = serializers.PVERoomSerializer(pve, context=self.get_serializer_context(), many=True).data

		return Response(relax + pve, status=status.HTTP_200_OK)

### MOB
# GET: /room/pve/{room_name}/mobs/
# GET: /mobs/{mob_name}
class RoomMobViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available mobs for the chosen PVE room
	'''
	serializer_class = serializers.MobSerializer

	def get_queryset(self):
		queryset = models.Mob.objects.all()
		room_name = self.kwargs.get('room_name')
		if room_name:
			queryset = queryset.filter(pveroom__name=room_name).all()
		return queryset

class MobViewSet(viewsets.GenericViewSet, generics.RetrieveAPIView):
	'''
		List of the available mobs for the chosen PVE room
	'''
	queryset = models.Mob.objects.all()
	serializer_class = serializers.MobSerializer
	lookup_field = 'name'

### ITEM
# GET: /room/relax/{room_name}/items/
# GET: /items/{pk}/
class ItemViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	model = models.Item
	serializer_class = serializers.ItemSerializer

class RoomItemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available items for the chosen relax room
	'''
	serializer_class = serializers.ItemSerializer

	def get_queryset(self):
		queryset = models.Item.objects.all()
		room_name = self.kwargs.get('room_name')
		if room_name:
			queryset = queryset.filter(relaxroom__name=room_name).all()
		return queryset


##############################################
# CHARACTER
class CharacterViewSet(viewsets.ModelViewSet):
	'''
		List of characters for the chosen user
	'''
	serializer_class = serializers.CharacterSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	lookup_field = 'name'

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

	# def partial_update(self, request, *args, **kwargs):
	# 	'''
	# 		Equip action
	# 	'''
	# 	character = self.get_object_or_none()
	# 	serializer = self.get_serializer(character, data=request.DATA, files=request.FILES, partial=True)

	# 	if not serializer.is_valid():
	# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	# 	if character.owner != request.user:
	# 		self.permission_denied(request)
	# 	item = models.Item.objects.get(pk=request.DATA.get('item'))

	# 	try:
	# 		record = models.InventoryRecord.objects.get(owner=character, item=item)
	# 	except ObjectDoesNotExist:
	# 		return Response(
	# 				data={'msg': 'The specified character does not own the specified item'},
	# 				status=status.HTTP_400_BAD_REQUEST
	# 			)

	# 	if item.item_type == 'W':
	# 		character.current_weapon = item
	# 	elif item.item_type == 'A':
	# 		character.current_armor = item
	# 	else:
	# 		return Response(
	# 				data={'msg': 'Cannot equip a restorative item'},
	# 				status=status.HTTP_400_BAD_REQUEST
	# 			)
	# 	character.save()
	# 	character = serializers.CharacterSerializer(character, context=self.get_serializer_context()).data
	# 	data = {
	# 		'msg': 'Item %s equipped' % item.name,
	# 		'character': character,
	# 	}

	# 	return Response(data=data)

class CharacterAbilityList(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the learned abilities for the chosen character
	'''
	def list(self, request, *args, **kwargs):
		name = self.kwargs.get('name')
		physical = models.PhysicalAbility.objects.filter(character__name=name).all()
		white = models.WhiteMagicAbility.objects.filter(character__name=name).all()
		black = models.BlackMagicAbility.objects.filter(character__name=name).all()

		physical = serializers.PhysicalAbilitySerializer(physical, context=self.get_serializer_context(), many=True).data
		white = serializers.WhiteMagicAbilitySerializer(white, context=self.get_serializer_context(), many=True).data
		black = serializers.BlackMagicAbilitySerializer(black, context=self.get_serializer_context(), many=True).data
		return Response(data={
					'physical': physical,
					'white_magic': white,
					'black_magic': black,
				})

	def next(self, request, *args, **kwargs):
		name = self.kwargs.get('name')
		if not name:
			raise ValueError("Please pass a character")

		physical = models.PhysicalAbility.objects.filter(character__name=name).all()
		white = models.WhiteMagicAbility.objects.filter(character__name=name).all()
		black = models.BlackMagicAbility.objects.filter(character__name=name).all()

		next_physical = models.PhysicalAbility.objects.filter(requires__in=physical).all()
		next_white = models.WhiteMagicAbility.objects.filter(requires__in=white).all()
		next_black = models.BlackMagicAbility.objects.filter(requires__in=black).all()

		next_physical = serializers.PhysicalAbilitySerializer(next_physical, context=self.get_serializer_context(), many=True).data
		next_white = serializers.WhiteMagicAbilitySerializer(next_white, context=self.get_serializer_context(), many=True).data
		next_black = serializers.BlackMagicAbilitySerializer(next_black, context=self.get_serializer_context(), many=True).data
		return Response(data={
					'physical': next_physical,
					'white_magic': next_white,
					'black_magic': next_black,
				})
	

class PhysicalAbilityDetail(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.PhysicalAbility.objects.all()
	serializer_class = serializers.PhysicalAbilitySerializer

class WhiteMagicAbilityDetail(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.WhiteMagicAbility.objects.all()
	serializer_class = serializers.WhiteMagicAbilitySerializer

class BlackMagicAbilityDetail(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.BlackMagicAbility.objects.all()
	serializer_class = serializers.BlackMagicAbilitySerializer

class InventoryRecordDetail(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
	queryset = models.InventoryRecord.objects.all()
	serializer_class = serializers.InventoryRecordSerializer

class CharacterInventory(viewsets.GenericViewSet,
							mixins.ListModelMixin, 
							mixins.CreateModelMixin,
							mixins.DestroyModelMixin):
	'''
		From this view it is possible for a character to buy (`POST`) items.
	'''
	queryset = models.InventoryRecord.objects
	serializer_class = serializers.InventoryRecordSerializer

	def get_queryset(self):
		return self.queryset.filter(owner__name=self.kwargs.get('name'))

	def create(self, request, *args, **kwargs):
		'''
			Buy action
		'''
		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if not serializer.is_valid:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


		character = models.Character.objects.get(name=self.kwargs.get('name'))
		if character.owner != request.user:
			self.permission_denied(request)
		item = models.Item.objects.get(pk=request.DATA.get('item'))

		if item.cost > character.guils:
			return Response(
						data={'msg': 'Not enough money to buy this item'},
					)

		try:
			record = models.InventoryRecord.objects.get(owner=character, item=item)
			record.quantity += 1
			record.save()
		except ObjectDoesNotExist:
			record = models.InventoryRecord.objects.create(owner=character, item=item)

		character.guils -= item.cost
		character.save()
		record = serializers.InventoryRecordSerializer(record, context=self.get_serializer_context()).data
		data = {
			'msg': 'Item %s added to inventory' % item.name,
			'inventory_record': record,
			'guils left': character.guils,
		}

		return Response(data=data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(data))

	def destroy(self, request, *args, **kwargs):
		'''
			Sell action
		'''
		character = models.Character.objects.get(name=self.kwargs.get('name'))
		if character.owner != request.user:
			self.permission_denied(request)
		item = models.Item.objects.get(pk=self.kwargs.get('pk'))

		try:
			record = models.InventoryRecord.objects.get(owner=character, item=item)
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