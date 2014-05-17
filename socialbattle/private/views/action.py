from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from socialbattle.private import models
from socialbattle.private import serializers
from socialbattle.private import mechanics
from django.db import models as dj_models
from rest_framework import serializers as drf_serializers
from socialbattle.private.tasks import update_status

def use_ability(attacker, attacked, ability):
	if ability not in attacker.abilities.all():
		return Response({'msg': 'You do not have the specified ability'}, status=status.HTTP_400_BAD_REQUEST)

	if ability.mp_required > attacker.curr_mp:
		return Response({'msg': 'The ability requires too much MPs'}, status=status.HTTP_400_BAD_REQUEST)

	#ct = mechanics.get_charge_time(attacker, ability)	
	ct = 10	
	dmg = mechanics.calculate_damage(attacker, attacked, ability)
	
	update_status.apply_async((attacker, attacked, dmg, ability), countdown=ct)

	data = {
		'dmg': dmg,
		'ct': ct,
	}
	return Response(data, status=status.HTTP_200_OK)

from socialbattle.private.tasks import end_battle as end_battle_task
def end_battle(character, mob, context):
	end_battle_task.delay(character, mob)
	data = {
		'msg': 'Battle ended, you win',
		'guils_gain': mob.guils,
		'ap_gain': mob.ap,
		'exp_gain': mob.exp,
		'level': character.level,
		'dropped': serializers.ItemSerializer(list(mob.drops.all()), context=context, many=True).data
	}
	return Response(data, status=status.HTTP_200_OK)

def use_item(character, item):
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
			'effect': effect,
			'curr_hp': character.curr_hp,
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

