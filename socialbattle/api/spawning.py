import threading
import time
import random
from socialbattle.api.models import PVERoom, Battle
from socialbattle.api.serializers import MobSerializer
from announce import AnnounceClient

class myThread(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(myThread, self).__init__()
		self.room = kwargs.pop('room', None)
		self.mobs = list(room.mobs.all())

	def run(self):
		print 'Starting thread for %s' % self.room.name
		mobs_no = len(self.mobs)
		while True:
			time.sleep(random.uniform(20, 60))
			mob = self.mobs[random.randint(0, mobs_no - 1)]
			#mob = MobSerializer(mob).data
			lock.acquire()
			#announce_client.broadcast(self.room.name, mob)
			## operation on db
			print 'Thread for %s: %s spawned' % (self.room.name, mob.name)
			lock.release()

#if __name__ == '__main__':
announce_client = AnnounceClient()
rooms = list(PVERoom.objects.all())
lock = threading.Lock()
for room in rooms:
	myThread(room=room).start()
			