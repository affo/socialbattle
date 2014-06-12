from oauth2_provider.oauth2_validators import OAuth2Validator
from social.backends.facebook import Facebook2OAuth2 as FacebookBackend
from social.apps.django_app.utils import load_strategy
from django.contrib.auth import authenticate

class MyOAuth2Validator(OAuth2Validator):
	def validate_user(self, username, password, client, request, *args, **kwargs):
		"""
		Check username and password correspond to a valid and active User, if fails
		try Facebook token authentication
		"""
		u = authenticate(username=username, password=password)
		if u is None or not u.is_active:
			u = self._authenticate_with_facebook(request)

		if u is not None and u.is_active:
			request.user = u
			return True

		return False

	def _authenticate_with_facebook(self, request):
		# WARNING! not rest_framework.Request, nor django.Request
		# but oauthlib.oauth.common.Request
		fb_token = getattr(request, 'fb_token', None)
		if not fb_token:
			return None
		strategy = load_strategy(backend='facebook')
		user = FacebookBackend(strategy=strategy).do_auth(fb_token)
		return user
