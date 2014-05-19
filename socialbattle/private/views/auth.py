from django.contrib.auth import login
from django.shortcuts import redirect
from social_auth.decorators import dsa_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from socialbattle.private.serializers import UserSerializer

@dsa_view()
@api_view(['GET', ])
@permission_classes([AllowAny, ])
def register_by_access_token(request, backend, *args, **kwargs):
    access_token = request.GET.get('access_token')
    user = backend.do_auth(access_token)
    if user and user.is_active:
    	print 'LOGGEDDDD'
        login(request, user)
    return Response(data=UserSerializer(user, context={'request': request}).data)