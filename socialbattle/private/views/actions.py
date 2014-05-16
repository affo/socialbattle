from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from socialbattle.private import models
from socialbattle.private import serializers

class Transaction(models.Model):
	OPERATION_TYPE = (('B', 'Buy'), ('S', 'Sell'), )
	character = models.ForeignKey(models.Character)

	item = models.ForeignKey(models.Item)
	quantity = models.IntegerField(default=0)
	operation = models.CharField(max_length=1, choices=OPERATION_TYPE)

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
	character = serializers.HyperlinkedRelatedField(
		view_name='character-detail',
		lookup_field='name',
		read_only=True,
	)

	class Meta:
		model = Transaction
		fields = ('character', 'item', 'quantity', 'operation', )

class AbilityUsage(models.Model):
	ability = models.ForeignKey(models.Ability)

class ItemUsage(models.Model):
	item = models.ForeignKey(models.Item)

class AbilityUsageSerializer(serializers.HyperlinkedModelSerializer):
	ability = serializers.HyperlinkedRelatedField(
		view_name='ability-detail',
		lookup_field='slug'
	)

	target = serializers.HyperlinkedRelatedField(
		view_name='target-detail',
		lookup_field='pk'
	)

	class Meta:
		model = AbilityUsage
		fields = ('ability', 'target')

class ItemUsageSerializer(serializers.HyperlinkedModelSerializer):
	item = serializers.HyperlinkedRelatedField(
		view_name='item-detail',
		lookup_field='slug'
	)

	target = serializers.HyperlinkedRelatedField(
		view_name='target-detail',
		lookup_field='pk'
	)

	class Meta:
		model = models.ItemUsage
		fields = ('item', 'target')

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
		record = serializers.InventoryRecordSerializer(record, context=self.get_serializer_context()).data
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
	#queryset = models.Battle.objects.all()
	#serializer_class = serializers.BattleSerializer

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
#	queryset = models.Battle.objects.all()
#	serializer_class = serializers.BattleSerializer

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
		target = serializer.object.target

		if ability not in character.abilities.all():
			return Response({'msg': 'You do not have the specified ability'}, status=status.HTTP_400_BAD_REQUEST)

		if ability.mp_required > character.curr_mp:
			return Response({'msg': 'The ability requires too much MPs'}, status=status.HTTP_400_BAD_REQUEST)

		#perform the attack
		ct = get_charge_time(character, ability)
		time.sleep(ct) #charging the ability

		try:
			target = target.mobsnapshot
		except ObjectDoesNotExist:
			target = target.character
		
		dmg = calculate_damage(character, target, ability)
		character.update_mp(ability)
		target.update_hp(dmg)

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