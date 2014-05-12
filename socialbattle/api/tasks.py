from __future__ import absolute_import

from celery import shared_task
import random
import time

@shared_task
def spawn(room_slug, mobs):
	print 'Starting task for %s' % room_slug
	mobs_no = len(mobs)
	time.sleep(random.uniform(20, 60))
	mob = mobs[random.randint(0, mobs_no - 1)]
	#mob = MobSerializer(mob).data
	#announce_client.broadcast(self.room.name, mob)
	## operation on db
	print 'Task for %s: %s spawned' % (room_slug, mob.name)