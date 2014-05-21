from django.contrib.auth import login
from django.shortcuts import redirect
from social_auth.decorators import dsa_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from socialbattle.private.serializers import UserSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

@dsa_view()
@api_view(['GET', ])
@permission_classes([AllowAny, ])
def register_by_access_token(request, backend, *args, **kwargs):
	access_token = request.GET.get('access_token')
	user = backend.do_auth(access_token)
	if user and user.is_active:
		token, created = Token.objects.get_or_create(user=user)
		return Response({'username': user.username,'token': token.key})
	return Response(status=status.HTTP_400_BAD_REQUEST)
