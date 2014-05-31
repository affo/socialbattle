from rest_framework.response import Response
from rest_framework import status
from socialbattle.private import models
from socialbattle.private import serializers
from socialbattle.private import mechanics
from socialbattle.private.models import Ability

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

from socialbattle.private.tasks import end_battle as end_battle_task
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

