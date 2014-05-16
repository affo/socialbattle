from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from socialbattle.private import models
from socialbattle.private import serializers

### MOB
# GET: /room/pve/{room_slug}/mobs/
# GET: /mobs/{mob_name}
class RoomMobViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available mobs for the chosen PVE room
	'''
	serializer_class = serializers.MobSerializer

	def get_queryset(self):
		queryset = models.Mob.objects.all()
		room_slug = self.kwargs.get('room_slug')
		if room_slug:
			queryset = queryset.filter(pveroom__slug=room_slug).all()
		return queryset

class MobViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	'''
		List of the available mobs for the chosen PVE room
	'''
	queryset = models.Mob.objects.all()
	serializer_class = serializers.MobSerializer
	lookup_field = 'slug'