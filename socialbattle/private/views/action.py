from rest_framework.response import Response
from rest_framework import status
from socialbattle.private import models
from socialbattle.private import serializers
from socialbattle.private.tasks import update_status
from socialbattle.private import mechanics

def use_ability(attacker, attacked, ability):
	if ability not in attacker.abilities.all():
		return Response({'msg': 'You do not have the specified ability'}, status=status.HTTP_400_BAD_REQUEST)

	if ability.mp_required > attacker.curr_mp:
		return Response({'msg': 'The ability requires too much MPs'}, status=status.HTTP_400_BAD_REQUEST)

	#ct = mechanics.get_charge_time(attacker, ability)	
	ct = 10	
	dmg = mechanics.calculate_damage(attacker, attacked, ability)
	
	try:
		update_status.apply_async((attacker, attacked, dmg, ability), countdown=ct)
	except:
		update_status(attacker, attacked, dmg, ability)

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

