from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api import mechanics
from socialbattle.api.models import Ability
from socialbattle.api import fake_serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

def use_ability(attacker, attacked, ability):
	if ability not in attacker.abilities.all():
		return Response({'msg': 'You do not have the specified ability'}, status=status.HTTP_400_BAD_REQUEST)

	if ability.mp_required > attacker.curr_mp:
		return Response({'msg': 'The ability requires too much MPs'}, status=status.HTTP_400_BAD_REQUEST)

	item_or_ability = ability
	if ability.element == Ability.ELEMENTS[6][0]:
		#physical ability
		if(attacker.weapon): 
			item_or_ability = attacker.weapon.item
		else:
			item_or_ability = None

	ct = mechanics.get_charge_time(attacker, item_or_ability)	
	dmg = mechanics.calculate_damage(attacker, attacked, ability)

	attacker_mp = attacker.update_mp(ability)
	attacked_hp = attacked.update_hp(dmg)

	data = {
		'dmg': dmg,
		'ct': ct,
		'attacker_mp': attacker_mp,
		'attacked_hp': attacked_hp,
	}
	return Response(data, status=status.HTTP_200_OK)

from socialbattle.api.tasks import end_battle as end_battle_task
def end_battle(character, mob, context):
	try:
		end_battle_task.delay(character, mob)
	except:
		end_battle_task(character, mob)

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
	if item not in character.inventory.all():
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

##########

@api_view(['POST'])
@permission_classes([AllowAny])
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
	serializer = fake_serializers.AttackSerializer(data=request.DATA)
	if serializer.is_valid():
		attacker = serializer.object.attacker
		attacked = serializer.object.attacked
		ability = serializer.object.ability
		dmg = mechanics.calculate_damage(attacker, attacked, ability)
		return Response({'dmg': dmg}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def exp(request, *args, **kwargs):
	'''
	Calculates the experience required to reach the specified level.    
	Sample input:

		{
			"lvl": 42
		}
	'''
	try:
		level = request.DATA['lvl']
		return Response({'exp': mechanics.get_exp(level)}, status=status.HTTP_200_OK)
	except:
		return Response({'lvl': 'this field is required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def ct(request, *args, **kwargs):
	'''
	Calculates the charge time required to perform an attack, given:  
	- the speed of the attacker  
	- the charge time factor of the ability (in case of magics)  
	- the charge time factor of the weapon (in case of physical attack)  
	Sample input:

		{
			"spd": 18,
			"ctf": 30
		}
	'''
	serializer = fake_serializers.CtSerializer(data=request.DATA)
	if serializer.is_valid():
		obj = serializer.object
		ct = mechanics.get_charge_time(obj, obj)
		return Response({'ct': ct}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def stat(request, *args, **kwargs):
	'''
	Calculates the stat specified from the level given.  
	The stat could be: `HP`, `MP`, `STR`, `MAG`, `SPD` or `VIT`.  
	Sample input:

		{
			"lvl": 25,
			"stat": "HP"
		}
	'''
	serializer = fake_serializers.StatSerializer(data=request.DATA)
	if serializer.is_valid():
		obj = serializer.object
		stat = mechanics.get_stat(obj.lvl, obj.stat)
		return Response({obj.stat: stat}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


