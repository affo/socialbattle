from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsOwner

class PVERoomMobList(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available mobs for the chosen PVE room
	'''
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
	'''
		List of characters for the chosen user
	'''
	queryset = models.Character.objects
	serializer_class = serializers.CharacterSerializer

	def get_queryset(self):
		return self.queryset.filter(owner__username=self.kwargs.get('username'))

	def pre_save(self, obj):
		obj.owner = self.request.user

	def post_save(self, obj, created=False):
		if created:
			obj.physical_abilities.add(models.PhysicalAbility.objects.get(name='attack'))
			obj.white_magic_abilities.add(models.WhiteMagicAbility.objects.get(name='cure'))
			obj.black_magic_abilities.add(models.BlackMagicAbility.objects.get(name='fire'))
			obj.black_magic_abilities.add(models.BlackMagicAbility.objects.get(name='thunder'))
			potion = models.Item.objects.get(name='potion')
			record = models.InventoryRecord.create(owner=obj, item=potion, quantity=3)
			obj.items.add(record)

class CharacterDetail(viewsets.GenericViewSet,
						mixins.DestroyModelMixin,
						mixins.RetrieveModelMixin,
						mixins.UpdateModelMixin):
	queryset = models.Character.objects.all()
	serializer_class = serializers.CharacterSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	lookup_field = 'name'

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

class CharacterNextAbilityList(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		This view returns the next abilities which the current character can learn.
	'''
	def list(self, request, *args, **kwargs):
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

class CharacterItemList(viewsets.GenericViewSet, mixins.ListModelMixin):
	queryset = models.InventoryRecord.objects
	serializer_class = serializers.InventoryRecordSerializer

	def get_queryset(self):
		return self.queryset.filter(owner__name=self.kwargs.get('name'))

class RelaxRoomDetail(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	model = models.RelaxRoom
	serializer_class = serializers.RelaxRoomSerializer
	lookup_field = 'name'

class PVERoomList(generics.ListAPIView):
	model = models.PVERoom
	serializer_class = serializers.PVERoomSerializer

class PVERoomDetail(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	model = models.PVERoom
	serializer_class = serializers.PVERoomSerializer
	lookup_field = 'name'

class ItemDetail(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	'''
		From this view it is possible for a character to buy (`/buy`) or sell (`/sell`) items.  
		Query parameters:  
			*	to buy: `/buy/?char=<character_name>&room=<room_name>`  
			*	to sell: `/sell/?char=<character_name>`  
			*	to equip: `/equip/?char=<character_name>`
	'''
	model = models.Item
	serializer_class = serializers.ItemSerializer

	@action(methods=['GET'])
	def buy(self, request, *args, **kwargs):
		try:
			name = request.QUERY_PARAMS['char']
			room = request.QUERY_PARAMS['room']
		except:
			return Response(
					data={'msg': 'Missing query params(): ?char=<character_name>&room=<room_name>'},
					status=status.HTTP_400_BAD_REQUEST
				)

		character = models.Character.objects.get(name=name)
		if character.owner != request.user:
			self.permission_denied(request)
		room = models.RelaxRoom.objects.get(name=room)
		item = models.Item.objects.get(pk=self.kwargs.get('pk'))

		if item not in room.sells.all():
			return Response(
					data={'msg': 'The specified room does not sell the specified item'},
					status=status.HTTP_400_BAD_REQUEST
				)

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

		return Response(data=data)
		

	@action(methods=['GET'])
	def sell(self, request, *args, **kwargs):
		try:
			name = request.QUERY_PARAMS['char']
		except:
			return Response(
					data={'msg': 'Missing query params(): ?char=<character_name>'},
					status=status.HTTP_400_BAD_REQUEST
				)

		character = models.Character.objects.get(name=name)
		if character.owner != request.user:
			self.permission_denied(request)
		item = models.Item.objects.get(pk=self.kwargs.get('pk'))

		try:
			record = models.InventoryRecord.objects.get(owner=character, item=item)
			record.quantity -= 1
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

	@action(methods=['GET'])
	def equip(self, request, *args, **kwargs):
		try:
			name = request.QUERY_PARAMS['char']
		except:
			return Response(
					data={'msg': 'Missing query params(): ?char=<character_name>'},
					status=status.HTTP_400_BAD_REQUEST
				)

		character = models.Character.objects.get(name=name)
		if character.owner != request.user:
			self.permission_denied(request)
		item = models.Item.objects.get(pk=self.kwargs.get('pk'))

		try:
			record = models.InventoryRecord.objects.get(owner=character, item=item)
		except ObjectDoesNotExist:
			return Response(
					data={'msg': 'The specified character does not own the specified item'},
					status=status.HTTP_400_BAD_REQUEST
				)

		if item.item_type == 'W':
			character.current_weapon = item
		elif item.item_type == 'A':
			character.current_armor = item
		else:
			return Response(
					data={'msg': 'Cannot equip a restorative item'},
					status=status.HTTP_400_BAD_REQUEST
				)
		character.save()
		character = serializers.CharacterSerializer(character, context=self.get_serializer_context()).data
		data = {
			'msg': 'Item %s equipped' % item.name,
			'character': character,
		}

		return Response(data=data)

class RoomList(generics.ListAPIView):
	def get(self, request, format=None):
		relax = models.RelaxRoom.objects.all()
		pve = models.PVERoom.objects.all()

		relax = serializers.RelaxRoomSerializer(relax, context=self.get_serializer_context()).data
		pve = serializers.PVERoomSerializer(pve, context=self.get_serializer_context()).data

		return Response(relax + pve)