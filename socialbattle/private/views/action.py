from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from socialbattle.private import models
from socialbattle.private import serializers
from django.db import models as dj_models
from rest_framework import serializers as drf_serializers

class AbilityUsage(dj_models.Model):
	ability = dj_models.ForeignKey(models.Ability)

class ItemUsage(dj_models.Model):
	item = dj_models.ForeignKey(models.Item)

class AbilityUsageSerializer(drf_serializers.HyperlinkedModelSerializer):
	ability = drf_serializers.HyperlinkedRelatedField(
		view_name='ability-detail',
		lookup_field='slug'
	)

	target = drf_serializers.HyperlinkedRelatedField(
		view_name='target-detail',
		lookup_field='pk'
	)

	class Meta:
		model = AbilityUsage
		fields = ('ability', 'target')

class ItemUsageSerializer(drf_serializers.HyperlinkedModelSerializer):
	item = drf_serializers.HyperlinkedRelatedField(
		view_name='item-detail',
		lookup_field='slug'
	)

	target = drf_serializers.HyperlinkedRelatedField(
		view_name='target-detail',
		lookup_field='pk'
	)

	class Meta:
		model = ItemUsage
		fields = ('item', 'target')

### ACTION
# POST: /characters/{character_name}/battles/
# GET: /battles/{pk}/
# POST: /battles/{pk}/abilities/
# POST: /battles/{pk}/items/
import time
class ActionMixin(object):

	@action(methods=['POST', ], serializer_class=AbilityUsageSerializer)
	def use_ability(self, request, *args, **kwargs):
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
	def use_item(self, request, *args, **kwargs):
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


class Target(dj_models.Model):
	atk = dj_models.IntegerField(default=0)
	stre = dj_models.IntegerField(default=0)
	mag = dj_models.IntegerField(default=0)
	defense = dj_models.IntegerField(default=0)
	mdefense = dj_models.IntegerField(default=0)
	level = dj_models.IntegerField(default=0)

class Ability(dj_models.Model):
	power = dj_models.IntegerField(default=0)
	element = dj_models.CharField(
			max_length=1,
			choices=models.Ability.ELEMENTS,
			default=models.Ability.ELEMENTS[0][0],
	)

class Attack(dj_models.Model):
	attacker = dj_models.ForeignKey(Target)
	attacked = dj_models.ForeignKey(Target)
	ability = dj_models.ForeignKey(Ability)

class TargetSerializer(drf_serializers.ModelSerializer):
	class Meta:
		model = Target
		fields = ('atk', 'stre', 'mag', 'defense', 'mdefense', 'level')
	

class AbilitySerializer(drf_serializers.ModelSerializer):
	element = drf_serializers.CharField(required=False)
	class Meta:
		model = Ability
		fields = ('power', 'element')

class AttackSerializer(drf_serializers.ModelSerializer):
	attacker = TargetSerializer()
	attacked = TargetSerializer()
	ability = AbilitySerializer()

	class Meta:
		model = Attack
		fields = ('attacker', 'attacked', 'ability')

from socialbattle.private import mechanics
from rest_framework.decorators import api_view
@api_view(['POST'])
def damage(request, *args, **kwargs):
	'''
	Calculates the damage giving an attacker, the target and the ability used.  
	Sample input:

		{
			"attacker": {
				"level": 2,
				"stre": 8,
				"mag": 5,
				"defense": 4,
				"mdefense": 7,
				"atk": 8
			},

			"attacked": {
				"level": 2,
				"stre": 8,
				"mag": 5,
				"defense": 4,
				"mdefense": 7,
				"atk": 8
			},

			"ability": {
				"power": 5,
				"element": "N"
			}
		}
	'''
	serializer = AttackSerializer(data=request.DATA)
	if serializer.is_valid():
		attacker = serializer.object.attacker
		attacked = serializer.object.attacked
		ability = serializer.object.ability
		dmg = mechanics.calculate_damage(attacker, attacked, ability)
		return Response({'dmg': dmg}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


