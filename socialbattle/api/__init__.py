from socialbattle import settings
from pusher import Pusher, pusher_from_url
from django.core.serializers.json import DjangoJSONEncoder

pusher = Pusher(
	app_id=settings.PUSHER_APP_ID,
	key=settings.PUSHER_APP_KEY,
	secret=settings.PUSHER_APP_SECRET,
	encoder=DjangoJSONEncoder
)