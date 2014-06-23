from socialbattle.api import tasks

class NotifyMixin(object):

	def notify(self, user, event, data):
		try:
			tasks.notify_user.delay(
				user=user,
				data=data,
				ctx=self.get_serializer_context(),
				event=event,
				create=True
			)
		except:
			tasks.notify_user(
				user=user,
				data=data,
				ctx=self.get_serializer_context(),
				event=event,
				create=True
			)