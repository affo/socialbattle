from __future__ import absolute_import

from celery import shared_task
import random, time
from socialbattle.api.models import PVERoom, Battle
from announce import AnnounceClient
announce_client = AnnounceClient()

@shared_task
def spawn(room):
	room_slug = room.slug
	mobs = list(room.mobs.all())
	mobs_no = len(mobs)
	mob = mobs[random.randint(0, mobs_no - 1)]
	data = {'mob_pk': mob.pk}
	try:
		announce_client.broadcast(room.slug, data)
	except:
		pass
	print 'Task for %s: %s spawned' % (room_slug, mob.name)

@shared_task
def spawn_beat():
	'''
		Periodic task configured in settings.py that spawns random monsters in all rooms
	'''
	rooms = list(PVERoom.objects.all())
	for room in rooms:
		cd = random.uniform(0, 5)
		spawn.apply_async((room, ), countdown=cd)

from socialbattle.api.mechanics import calculate_damage, get_charge_time
@shared_task
def fight(battle_pk):
	'''
		"periodical" task started by a mob until the battle is alive
	'''
	battle = Battle.objects.get(pk=battle_pk)
	if battle.mob_hp > 0 and battle.character.curr_hp > 0: #the mob is still alive
		abilities = list(battle.mob.abilities.all())
		abilities_no = len(abilities)
		ability = abilities[random.randint(0, abilities_no - 1)]
		ct = get_charge_time(battle.mob, ability)
		print 'Battle %s: mob %s charging %s --> ct %fs' % (battle.pk, battle.mob.name, ability.name, ct)
		time.sleep(ct) #charging the ability

		dmg = calculate_damage(battle.mob, battle.character, ability)
		battle.assign_damage_to_character(dmg)
		print 'Battle %s: mob %s uses %s --> dmg %d' % (battle.pk, battle.mob.name, ability.name, dmg)
		
		fight.apply_async((battle_pk, ), countdown=random.uniform(2, 5))
	else:
		print 'Battle %s: mob %s is dead or character is dead, battle ended' % (battle.pk, battle.mob.name)
		battle.delete()