from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsOwner, IsOwnedByCharacter
from socialbattle.api.helpers import TransactionSerializer, AbilityUsageSerializer, ItemUsageSerializer
from socialbattle.api.mechanics import calculate_damage, get_charge_time, get_exp, get_stat

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
class CharacterAbilityViewSet(viewsets.GenericViewSet,
								mixins.ListModelMixin,
								mixins.CreateModelMixin):
	'''
		List of the learned abilities for the chosen character
	'''
	serializer_class = AbilityUsageSerializer

	def list(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		abilities = character.abilities.all()
		abilities = serializers.AbilitySerializer(abilities, context=self.get_serializer_context(), many=True).data
		return Response(data=abilities, status=status.HTTP_200_OK)

	def create(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		serializer = self.get_serializer(data=request.DATA)

		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		ability = serializer.object.ability

		if ability not in character.abilities.all():
			return Response({'msg': 'You do not have the specified ability'}, status=status.HTTP_400_BAD_REQUEST)

		if ability.element != models.Ability.ELEMENTS[5][0]:
			return Response({'msg': 'Can use only white magic abilities'}, status=status.HTTP_400_BAD_REQUEST)

		if ability.mp_required > character.curr_mp:
			return Response({'msg': 'The ability requires too much MPs'}, status=status.HTTP_400_BAD_REQUEST)
		dmg = calculate_damage(character, None, ability)
		character.update_mp(ability)
		character.update_hp(dmg)
		character.save()

		data = {
			'effect': dmg,
			'curr_hp': character.curr_hp,
			'mp_left': character.curr_mp,
			'mp_spent': ability.mp_required,
		}
		return Response(data, status=status.HTTP_200_OK)

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
# GET: /characters/{character_name}/inventory/
class CharacterInventoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,):
	'''
		The inventory of the selected character.  
	'''
	serializer_class = serializers.InventoryRecordSerializer

	def get_queryset(self):
		queryset = models.InventoryRecord.objects.all()
		name = self.kwargs.get('character_name')
		if name:
			queryset = queryset.filter(owner__name=name)
		return queryset

class InventoryRecordViewSet(viewsets.GenericViewSet,
							mixins.RetrieveModelMixin,
							mixins.UpdateModelMixin,
							mixins.DestroyModelMixin):
	'''
		Detailed view of an inventory record:
		It is possible to equip (`PUT`) items.  
		It is possible to use (`DELETE`) restorative items.
	'''
	queryset = models.InventoryRecord.objects.all()
	serializer_class = serializers.InventoryRecordSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnedByCharacter]

	def pre_save(self, obj):
		print obj.equipped
		RESTORATIVE = models.Item.ITEM_TYPE[0][0]
		ARMOR = models.Item.ITEM_TYPE[2][0]
		WEAPON = models.Item.ITEM_TYPE[1][0]

		records = self.get_queryset().filter(owner=obj.owner).all()

		if obj.item.item_type == RESTORATIVE and obj.equipped == True:
			raise ValidationError({"msg": ["Cannot equip a restorative time"]})

		n_armor = records.filter(item__item_type=ARMOR).filter(equipped=True).count()
		if n_armor == 1 and obj.item.item_type == ARMOR and obj.equipped == True:
			raise ValidationError({"msg": ["Cannot equip two armors at the same time"]})

		n_weapon = records.filter(item__item_type=WEAPON).filter(equipped=True).count()
		print 'weapon: %s, armor %s' % (n_weapon, n_armor)
		if n_weapon == 1 and obj.item.item_type == WEAPON and obj.equipped == True:
			raise ValidationError({"msg": ["Cannot equip two weapons at the same time"]})

	def destroy(self, request, *args, **kwargs):
		record = self.get_object()
		character = record.owner
		item = record.item

		if item.item_type != models.Item.ITEM_TYPE[0][0]:
			return Response({'msg': 'You can use only restorative items'}, status=status.HTTP_400_BAD_REQUEST)

		effect = item.get_restorative_effect(character)
		character.update_hp(-effect)
		record.quantity -= 1
		if record.quantity == 0:
			record.delete()
		else:
			record.save()
		data = {
				'effect': effect,
				'curr_hp': character.curr_hp,
				'inventory_record': self.get_serializer(record).data
			}
		return Response(data, status=status.HTTP_200_OK)

### TRANSACTION
# POST: /characters/{character_name}/transactions/
class TransactionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
	'''
		From this view it is possible for a character to buy and sell items.
	'''
	serializer_class = TransactionSerializer

	def create(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		if character.owner != request.user:
			self.permission_denied(request)

		BUY_OP = Transaction.OPERATION_TYPE[0][0]
		SELL_OP = Transaction.OPERATION_TYPE[1][0]

		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		transaction = serializer.object	

		if transaction.operation == BUY_OP:	
			if transaction.item.cost * transaction.quantity > character.guils and transaction.operation:
				return Response(
							data={'msg': 'Not enough money to buy this item'},
						)

			try:
				record = models.InventoryRecord.objects.get(owner=character, item=transaction.item)
				record.quantity += transaction.quantity
				record.save()
			except ObjectDoesNotExist:
				record = models.InventoryRecord.objects.create(
							owner=character,
							item=transaction.item, 
							quantity=transaction.quantity
						)

			character.guils -= (transaction.item.cost * transaction.quantity)

		elif transaction.operation == SELL_OP:
			try:
				record = models.InventoryRecord.objects.get(owner=character, item=transaction.item)
				if transaction.quantity > record.quantity:
					return Response(
							data={'msg': 'You do not have as much items of that type'},
							status=status.HTTP_400_BAD_REQUEST
						)

				record.quantity -= transaction.quantity
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

			character.guils += (transaction.item.cost / 2) * transaction.quantity

		character.save()
		record = serializers.InventoryRecordUpdateSerializer(record, context=self.get_serializer_context()).data
		data = {
			'inventory_record': record,
			'guils left': character.guils,
		}

		return Response(data=data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(data))

### BATTLE
# POST: /characters/{character_name}/battles/
# GET: /battles/{pk}/
# POST: /battles/{pk}/abilities/
# POST: /battles/{pk}/items/
import random
class CharacterBattleViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
	queryset = models.Battle.objects.all()
	serializer_class = serializers.BattleSerializer

	def pre_save(self, obj):
		character = get_object_or_404(models.Character.objects.all(), name=self.kwargs.get('character_name'))
		obj.character = character
		mobs = list(obj.room.mobs.all())
		mobs_no = len(mobs)
		mob = mobs[random.randint(0, mobs_no - 1)]
		obj.mob_snapshot = models.MobSnapshot.objects.create(mob=mob,
								curr_hp=mob.hp, curr_mp=mob.mp,
								max_hp=mob.hp, max_mp=mob.hp)

	def post_save(self, obj, created=False):
		if created:
			from socialbattle.api.tasks import fight
			fight.delay(obj.pk) #starts mob's AI

import time
class BattleViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.Battle.objects.all()
	serializer_class = serializers.BattleSerializer

	@action(methods=['POST', ], serializer_class=AbilityUsageSerializer)
	def abilities(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA)

		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		battle = self.get_object()
		character = battle.character
		mob_snapshot = battle.mob_snapshot
		mob = mob_snapshot.mob
		ability = serializer.object.ability

		if ability not in character.abilities.all():
			return Response({'msg': 'You do not have the specified ability'}, status=status.HTTP_400_BAD_REQUEST)

		if ability.mp_required > character.curr_mp:
			return Response({'msg': 'The ability requires too much MPs'}, status=status.HTTP_400_BAD_REQUEST)

		#perform the attack
		ct = get_charge_time(character, ability)
		time.sleep(ct) #charging the ability
		
		dmg = calculate_damage(character, mob_snapshot, ability)
		character.update_mp(ability)
		if ability.element == models.Ability.ELEMENTS[5][0]: #white magic
			character.update_hp(dmg)
		else:
			mob_snapshot.update_hp(dmg)

		if mob_snapshot.curr_hp <= 0: #battle ended, you win
			drops = list(mob.drops.all())
			earned_items = []
			for item in drops:
				earned_items.append(item)
				try:
					record = models.InventoryRecord.objects.get(owner=character, item=item)
					record.quantity += 1
					record.save()
				except ObjectDoesNotExist:
					record = models.InventoryRecord.objects.create(
								owner=character,
								item=item, 
							)

			character.ap += mob.ap
			character.guils += mob.guils
			character.exp += mob.exp
			diff_level = 0
			while character.exp >= get_exp(character.level + 1):
				character.level += 1
				diff_level += 1

			#update character statistics
			old_hp = character.max_hp
			old_mp = character.max_mp
			old_stre = character.stre
			old_spd = character.spd
			old_mag = character.mag
			old_vit = character.vit
			if diff_level > 0:
				character.max_hp = get_stat(character.level, 'HP')
				character.max_mp = get_stat(character.level, 'MP')
				character.stre = get_stat(character.level, 'STR')
				character.spd = get_stat(character.level, 'SPD')
				character.mag = get_stat(character.level, 'MAG')
				character.vit = get_stat(character.level, 'VIT')

			character.save()
			data = {
				'msg': 'Battle ended, you win',
				'guils': mob.guils,
				'ap': mob.ap,
				'exp': mob.exp,
				'levels_earned': diff_level,
				'hp_gain': character.max_hp - old_hp,
				'mp_gain': character.max_mp - old_mp,
				'str_gain': character.stre - old_stre,
				'spd_gain': character.spd - old_spd,
				'mag_gain': character.mag - old_mag,
				'vit_gain': character.vit - old_vit,
				'dropped': serializers.ItemSerializer(
										earned_items,
										context=self.get_serializer_context(),
										many=True,
									).data
			}
		else:
			data = {
				'ability': serializer.data,
				'dmg': dmg,
				'mob_hp_left': mob_snapshot.curr_hp,
			}
		return Response(data, status=status.HTTP_200_OK)			

	@action(methods=['POST', ], serializer_class=ItemUsageSerializer)
	def items(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA)

		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		battle = self.get_object()
		character = battle.character
		item = serializer.object.item

		if item not in character.items.all():
			return Response({'msg': 'You do not have the specified item'}, status=status.HTTP_400_BAD_REQUEST)

		if item.item_type != models.Item.ITEM_TYPE[0][0]:
			return Response({'msg': 'You can use only restorative items'}, status=status.HTTP_400_BAD_REQUEST)

		effect = item.get_restorative_effect(character)
		character.update_hp(-effect)
		record = models.InventoryRecord.objects.get(owner=character, item=item)
		record.quantity -= 1
		if record.quantity == 0:
			record.delete()
		else:
			record.save()
		data = {
				'item': serializer.data,
				'effect': effect,
				'curr_hp': character.curr_hp,
				'inventory_record': serializers.InventoryRecordSerializer(record,
									context=self.get_serializer_context()).data
			}
		return Response(data, status=status.HTTP_200_OK)