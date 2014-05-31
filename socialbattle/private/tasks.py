from __future__ import absolute_import

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from socialbattle.private.models import InventoryRecord
from socialbattle.private import mechanics
import random, time

@shared_task
def end_battle(character, mob):
	# add dropped items
	drops = list(mob.drops.all())
	for item in drops:
		try:
			record = InventoryRecord.objects.get(owner=character, item=item)
			record.quantity += 1
			record.save()
		except ObjectDoesNotExist:
			record = InventoryRecord.objects.create(
						owner=character,
						item=item, 
					)

	#update aps, guils, exp and level
	character.ap += mob.ap
	character.guils += mob.guils
	character.exp += mob.exp
	diff_level = 0
	while character.exp >= mechanics.get_exp(character.level + 1):
		character.level += 1
		diff_level += 1

	#update stats
	if diff_level > 0:
		character.max_hp = mechanics.get_stat(character.level, 'HP')
		character.max_mp = mechanics.get_stat(character.level, 'MP')
		character.stre = mechanics.get_stat(character.level, 'STR')
		character.spd = mechanics.get_stat(character.level, 'SPD')
		character.mag = mechanics.get_stat(character.level, 'MAG')
		character.vit = mechanics.get_stat(character.level, 'VIT')

	character.save()