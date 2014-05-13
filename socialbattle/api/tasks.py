from __future__ import absolute_import

from celery import shared_task
import random
import time

from socialbattle.api.models import PVERoom

@shared_task
def spawn(room):
	room_slug = room.slug
	mobs = list(room.mobs.all())
	mobs_no = len(mobs)
	mob = mobs[random.randint(0, mobs_no - 1)]
	#mob = MobSerializer(mob).data
	#announce_client.broadcast(self.room.name, mob)
	## operation on db
	print 'Task for %s: %s spawned' % (room_slug, mob.name)

@shared_task
def spawn_beat():
	rooms = list(PVERoom.objects.all())
	for room in rooms:
		cd = random.uniform(0, 5)
		spawn.apply_async((room, ), countdown=cd)