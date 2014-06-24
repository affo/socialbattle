from socialbattle.api import tasks

class NotifyMixin(object):
	_task = None

	def _notify(self, *args):
		ctx = self.get_serializer_context()
		try:
			self._task.delay(*args, ctx=ctx)
		except:
			self._task(*args, ctx=ctx)

	def notify(self, user, event, data, create=False):
		self._task = tasks.notify_user
		self._notify(user, event, data, create)

	def notify_followers(self, user, event, data, create=False):
		self._task = tasks.notify_followers
		self._notify(user, event, data, create)

	def push_comment(self, comment):
		self._task = tasks.push_comment
		self._notify(comment)

	def push_post(self, post):
		self._task = tasks.push_post
		self._notify(post)

	def notify_commentors(self, user, post, data, event, create=False):
		self._task = tasks.notify_commentors
		self._notify(user, post, data, event, create)