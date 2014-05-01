from rest_framework import permissions
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers

#from announce import AnnounceClient
#announce_client = AnnounceClient()

@api_view(['GET'])
@permission_classes([permissions.AllowAny, ])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'rooms': reverse('room-list', request=request, format=format),
		'characters': reverse('character-list', request=request, format=format),
		})


#remember:
# Custom actions which use the @link decorator will respond to GET requests.
# We could have instead used the @action decorator if we wanted an action that responded to POST requests.
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

@api_view(['POST', ])
@renderer_classes((JSONRenderer, ))
def signup(request, format=None):
		username = request.DATA['username']
		password = request.DATA['password']
		email = request.DATA['email']

		user = models.User.objects.create_user(username, email, password)
		user = serializers.UserSerializer(user).data
		return Response(user)

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
@api_view(['POST', ])
@renderer_classes((JSONRenderer, ))
@permission_classes([permissions.IsAuthenticated, ])
def signout(request, format=None):
	logout(request)
	return Response(
			data={'message': 'Logged out successfully'},
			status=status.HTTP_200_OK
			)

@api_view(['GET', ])
@renderer_classes((JSONRenderer, ))
@permission_classes([permissions.IsAuthenticated, ])
def search_user(request, format=None):
		query = request.DATA['query']

		from django.db.models import Q
		users = models.User.objects.filter(
				Q(username__icontains=query) |
				Q(first_name__icontains=query) |
				Q(last_name__icontains=query)
			)

		return Response(serializers.UserSerializer(users).data)

@api_view(['GET', ])
@renderer_classes((JSONRenderer, ))
@permission_classes([permissions.IsAuthenticated, ])
def search_character(request, format=None):
		query = request.DATA['query']
		characters = models.Character.objects.filter(name__icontains=query)
		return Response(serializers.CharacterSerializer(characters).data)

#modify the model accordingly
@api_view(['GET', ])
@renderer_classes((JSONRenderer, ))
@permission_classes([permissions.IsAuthenticated, ])
def search_room(request, format=None):
		query = request.DATA['query']
		rooms = models.Room.objects.filter(name__icontains=query)
		return Response(serializers.RoomSerializer(rooms).data)