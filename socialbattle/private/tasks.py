from __future__ import absolute_import

from celery import shared_task
import random, time
from socialbattle.api.models import PVERoom, Battle, MobSnapshot, Ability
from announce import AnnounceClient
announce_client = AnnounceClient()

# @shared_task
# def spawn(room):
# 	room_slug = room.slug
# 	mobs = list(room.mobs.all())
# 	mobs_no = len(mobs)
# 	mob = mobs[random.randint(0, mobs_no - 1)]
# 	MobSnapshot.objects.create(mob=mob, room=room,
# 								curr_hp=mob.hp, curr_mp=mob.mp,
# 								max_hp=mob.hp, max_mp=mob.hp)
# 	data = {'msg': 'mob spawned in room %s' % room_slug}
# 	try:
# 		announce_client.broadcast(room.slug, data)
# 	except:
# 		pass
# 	print 'Task for %s: %s spawned' % (room_slug, mob.name)

# @shared_task
# def spawn_beat():
# 	'''
# 		Periodic task configured in settings.py that spawns random monsters in all rooms
# 	'''
# 	rooms = list(PVERoom.objects.all())
# 	for room in rooms:
# 		cd = random.uniform(0, 5)
# 		spawn.apply_async((room, ), countdown=cd)

from socialbattle.api.mechanics import calculate_damage, get_charge_time
@shared_task
def fight(battle_pk):
	'''
		"periodical" task started by a mob until the battle is alive
	'''
	battle = Battle.objects.get(pk=battle_pk)
	mob_snapshot = battle.mob_snapshot
	mob = mob_snapshot.mob
	character = battle.character
	if mob_snapshot.curr_hp > 0 and character.curr_hp > 0: #the mob is still alive
		abilities = list(mob.abilities.all())
		abilities_no = len(abilities)
		ability = abilities[random.randint(0, abilities_no - 1)]
		ct = get_charge_time(mob, ability)
		print 'Battle %s: mob %s charging %s --> ct %fs' % (battle.pk, mob.name, ability.name, ct)
		time.sleep(ct) #charging the ability

		dmg = calculate_damage(mob_snapshot, character, ability)
		if ability.element == Ability.ELEMENTS[5][0]: #white magic
			mob_snapshot.update_hp(dmg)
		else:
			character.update_hp(dmg)

		msg = 'Battle %s: mob %s uses %s --> dmg %d' % (battle.pk, mob.name, ability.name, dmg)
		try:
			data = {
				'msg': msg,
				'dmg': dmg,
			}
	 		announce_client.broadcast(room.slug, data)
	 	except:
	 		pass

		print msg
		fight.apply_async((battle_pk, ), countdown=random.uniform(2, 5))
	else:
		print 'Battle %s: mob %s is dead or character is dead, battle ended' % (battle.pk, mob.name)
		battle.mob_snapshot.delete()
		battle.delete()