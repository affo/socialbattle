from socialbattle.api import tasks

class NotifyMixin(object):
	_task = None

	def _notify(self, user, event, data):
		try:
			self._task.delay(
				user=user,
				data=data,
				ctx=self.get_serializer_context(),
				event=event,
				create=True
			)
		except:
			self._task(
				user=user,
				data=data,
				ctx=self.get_serializer_context(),
				event=event,
				create=True
			)

	def notify(self, user, event, data):
		self._task = tasks.notify_user
		self._notify(user, event, data)

	def notify_followers(self, user, event, data):
		self._task = tasks.notify_followers
		self._notify(user, event, data)